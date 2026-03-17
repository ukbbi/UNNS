/**
 * Chamber XXXII — Main Pipeline Orchestrator
 * Implements Section 6.1 from Observability Paper
 * 
 * 5-Step Pipeline:
 * 1. Field Construction (6.1.1)
 * 2. Recursive Evolution (6.1.2)
 * 3. Collapse Application (Definition 2)
 * 4. Closure Metric (6.1.3)
 * 5. Null Ensemble + Stats (6.1.4 + 6.1.5)
 * 
 * @version 1.0.0
 * @phase Phase 1 (L5-Ready: Basic)
 */

import { CollapseOperator } from '../collapse/CollapseOperator.js';
import { TypeIVDetector } from '../observability/TypeIVDetector.js';
import { CorrectionEngine } from '../stats/CorrectionEngine.js';
import { computeClosureMetric } from './closureMetrics.js';
import { generateNullEnsemble } from './nullGenerator.js';
import { computeRunSignature } from '../repro/RunSignature.js';

/**
 * Run complete observability pipeline
 * 
 * @param {Object} config - Complete run configuration
 * @returns {Object} - Pipeline results with verdict
 */
export async function runPipeline(config) {
  const startTime = Date.now();
  
  const results = {
    success: false,
    config: config,
    stages: {},
    errors: [],
    warnings: [],
    verdict: null,
    signature: null,
    timing: {}
  };
  
  try {
    console.log('[Pipeline] Starting 5-step observability pipeline');
    
    // ========================================
    // STAGE 1: FIELD CONSTRUCTION (Section 6.1.1)
    // ========================================
    console.log('[Pipeline] Stage 1: Field Construction');
    const t1_start = Date.now();
    
    results.stages.fieldConstruction = await constructField(config.data, config.preprocessing);
    
    if (!results.stages.fieldConstruction.success) {
      throw new PipelineError('field_construction', results.stages.fieldConstruction.error);
    }
    
    results.timing.fieldConstruction = Date.now() - t1_start;
    console.log(`[Pipeline] Stage 1 complete (${results.timing.fieldConstruction}ms)`);
    
    // ========================================
    // STAGE 2: RECURSIVE EVOLUTION (Section 6.1.2)
    // ========================================
    console.log('[Pipeline] Stage 2: Recursive Evolution');
    const t2_start = Date.now();
    
    results.stages.evolution = await evolveField(
      results.stages.fieldConstruction.field,
      config.phi,
      config.psi,
      config.convergence
    );
    
    if (!results.stages.evolution.converged && !config.convergence.allowNonConvergence) {
      results.warnings.push({
        stage: 'evolution',
        severity: 'high',
        message: `Did not converge after ${config.convergence.N_max} iterations. May indicate Type II failure.`
      });
    }
    
    results.timing.evolution = Date.now() - t2_start;
    console.log(`[Pipeline] Stage 2 complete (${results.timing.evolution}ms, converged=${results.stages.evolution.converged})`);
    
    // ========================================
    // STAGE 3: COLLAPSE APPLICATION (Definition 2) — CRITICAL
    // ========================================
    console.log('[Pipeline] Stage 3: Collapse Application');
    const t3_start = Date.now();
    
    const collapseOp = new CollapseOperator(
      config.collapse.type,
      config.collapse.params,
      config.psi
    );
    
    // 3a: Validate Ψ-preservation (HARD REQUIREMENT)
    console.log('[Pipeline] Stage 3a: Validating Ψ-constraints');
    const psiValid = collapseOp.validatePsi(
      results.stages.evolution.finalField,
      config.psi
    );
    
    if (!psiValid) {
      throw new PipelineError(
        'collapse_psi_violation',
        `Collapse operator ${config.collapse.type} violates Ψ-constraints. Cannot proceed.`,
        {
          operator: config.collapse.type,
          params: config.collapse.params,
          psi: config.psi,
          suggestion: 'Choose different collapse operator or modify Ψ constraints'
        }
      );
    }
    
    // 3b: Apply collapse
    console.log('[Pipeline] Stage 3b: Applying collapse C: R → R\'');
    const collapsedField = collapseOp.apply(results.stages.evolution.finalField);
    
    // 3c: Test idempotence (WARNING if fails)
    console.log('[Pipeline] Stage 3c: Testing idempotence C(C(R)) ≈ C(R)');
    const idempotence = collapseOp.idempotentTest(results.stages.evolution.finalField);
    
    if (!idempotence.pass) {
      results.warnings.push({
        stage: 'collapse',
        severity: 'moderate',
        message: `Idempotence error: ${(idempotence.relative * 100).toFixed(2)}%. Collapse may not be stable.`,
        details: idempotence
      });
    }
    
    // 3d: Compute DOF reduction
    const dofMetric = collapseOp.destructionMetric(
      results.stages.evolution.finalField,
      collapsedField
    );
    
    results.stages.collapse = {
      field: collapsedField,
      operator: collapseOp.toJSON(),
      dofReduction: dofMetric,
      idempotence: idempotence,
      psiValid: true
    };
    
    results.timing.collapse = Date.now() - t3_start;
    console.log(`[Pipeline] Stage 3 complete (${results.timing.collapse}ms, DOF reduced by ${(dofMetric.reduction_percent).toFixed(1)}%)`);
    
    // ========================================
    // STAGE 4: CLOSURE METRIC (Section 6.1.3)
    // ========================================
    console.log('[Pipeline] Stage 4: Computing τ̂ closure metric');
    const t4_start = Date.now();
    
    results.stages.closureMetric = await computeClosureMetric(
      results.stages.fieldConstruction.field,  // F_0
      collapsedField,                           // F_final after collapse
      config.metric,
      results.stages.evolution
    );
    
    results.timing.closureMetric = Date.now() - t4_start;
    console.log(`[Pipeline] Stage 4 complete (${results.timing.closureMetric}ms, τ̂=${results.stages.closureMetric.value.toFixed(6)})`);
    
    // ========================================
    // STAGE 5: NULL ENSEMBLE (Section 6.1.4)
    // ========================================
    console.log('[Pipeline] Stage 5: Generating null ensemble');
    const t5_start = Date.now();
    
    results.stages.nulls = await generateNullEnsemble(
      config.data,
      config.nulls,
      {
        phi: config.phi,
        psi: config.psi,
        collapse: config.collapse,
        metric: config.metric,
        convergence: config.convergence,
        preprocessing: config.preprocessing
      }
    );
    
    results.timing.nullEnsemble = Date.now() - t5_start;
    console.log(`[Pipeline] Stage 5 complete (${results.timing.nullEnsemble}ms, N_null=${results.stages.nulls.N_null})`);
    
    // ========================================
    // STAGE 6: STATISTICAL TESTING (Section 6.1.5)
    // ========================================
    console.log('[Pipeline] Stage 6: Statistical testing with correction');
    const t6_start = Date.now();
    
    // Initialize correction engine
    const correctionEngine = config.correctionEngine || new CorrectionEngine();
    
    // Register this comparison
    correctionEngine.registerComparison(
      config.comparisonType || 'main_analysis',
      config.configHash
    );
    
    // Compute raw statistics
    const rawStats = computeStatistics(
      results.stages.closureMetric.value,
      results.stages.nulls.distribution,
      config.nulls
    );
    
    // Apply correction
    results.stages.stats = correctionEngine.correct(
      rawStats.pValue,
      config.correction.method || 'bonferroni',
      rawStats.cohensD
    );
    
    // Merge raw and corrected
    results.stages.stats = {
      ...rawStats,
      ...results.stages.stats,
      correctionEngine: correctionEngine.toJSON()
    };
    
    results.timing.statistics = Date.now() - t6_start;
    console.log(`[Pipeline] Stage 6 complete (${results.timing.statistics}ms, p_corrected=${results.stages.stats.p_corrected.toFixed(6)})`);
    
    // ========================================
    // STAGE 7: TYPE IV DETECTION (Section 7.4)
    // ========================================
    console.log('[Pipeline] Stage 7: Type IV failure detection');
    const t7_start = Date.now();
    
    const typeIV = new TypeIVDetector(config.storage || 'localStorage');
    
    const typeIV_result = typeIV.recordRun(
      {
        phi: config.phi,
        psi: config.psi,
        collapse: config.collapse,
        metric: config.metric,
        thresholds: config.thresholds
      },
      {
        verdict: results.stages.stats.overall_pass ? 'pass' : 'fail',
        passed: results.stages.stats.overall_pass,
        pValue: results.stages.stats.p_corrected,
        effectSize: results.stages.stats.cohensD
      },
      config.datasetId
    );
    
    results.stages.typeIV = typeIV_result;
    
    if (typeIV_result.triggered) {
      results.warnings.push({
        stage: 'epistemic',
        severity: 'critical',
        message: 'Type IV failure detected (invariance failure)',
        details: typeIV_result
      });
    }
    
    results.timing.typeIV = Date.now() - t7_start;
    console.log(`[Pipeline] Stage 7 complete (${results.timing.typeIV}ms, triggered=${typeIV_result.triggered})`);
    
    // ========================================
    // STAGE 8: VERDICT COMPUTATION (Section 7)
    // ========================================
    console.log('[Pipeline] Stage 8: Computing final verdict');
    
    results.verdict = computeVerdict(
      results.stages.stats,
      typeIV_result,
      results.warnings,
      results.stages.nulls
    );
    
    console.log(`[Pipeline] Verdict: ${results.verdict.outcome} (${results.verdict.type})`);
    
    // ========================================
    // SUCCESS
    // ========================================
    results.success = true;
    
  } catch (error) {
    // ========================================
    // ERROR HANDLING
    // ========================================
    console.error('[Pipeline] Error:', error);
    
    results.errors.push({
      stage: error.stage || 'unknown',
      message: error.message,
      details: error.details || null,
      fatal: true,
      timestamp: Date.now()
    });
    
    results.success = false;
    results.verdict = {
      outcome: 'ERROR',
      type: 'Pipeline Failure',
      message: error.message,
      stage: error.stage
    };
  } finally {
    // ========================================
    // FINALIZATION (Always runs)
    // ========================================
    
    // Compute total timing
    results.timing.total = Date.now() - startTime;
    
    // Always compute signature (even on failure, for debugging)
    results.signature = computeRunSignature(config, results);
    
    console.log(`[Pipeline] Complete (${results.timing.total}ms, success=${results.success})`);
  }
  
  return results;
}

/**
 * Compute final verdict with Type IV override logic
 * Implements Section 7 failure taxonomy
 */
function computeVerdict(stats, typeIV, warnings, nulls) {
  // TYPE IV OVERRIDES EVERYTHING (Section 7.4)
  if (typeIV.triggered) {
    return {
      outcome: 'FAILURE',
      type: 'Type IV: Invariance Failure',
      message: typeIV.recommendation.message,
      epistemic_status: 'Method failure, not necessarily substrate failure',
      severity: typeIV.severity,
      evidence: typeIV.evidence,
      paper_section: '7.4'
    };
  }
  
  // Check statistical significance (with correction)
  if (stats.significant && stats.overall_pass) {
    // Passed discrimination test
    
    if (warnings.length > 0) {
      // Warnings present - marginal success
      return {
        outcome: 'MARGINAL',
        type: 'Detection with warnings',
        message: `τ-closure detected (p_corrected = ${stats.p_corrected.toFixed(4)}, d = ${stats.cohensD.toFixed(2)}), but see warnings`,
        warnings: warnings,
        epistemic_status: 'Closure detected but quality concerns exist',
        paper_section: '5.2, 7'
      };
    }
    
    // Clean success
    return {
      outcome: 'SUCCESS',
      type: 'τ-closure detected',
      message: `Observable τ-closure: p_corrected = ${stats.p_corrected.toFixed(4)} < 0.01, d = ${stats.cohensD.toFixed(2)} > 0.8`,
      effect_size: stats.cohensD,
      discriminability: {
        level1: nulls.level1_passed,
        level2: nulls.level2_passed,
        level3: nulls.level3_passed
      },
      epistemic_status: 'Substrate observable under current projection',
      paper_section: 'Definition 5, Section 5.2'
    };
  }
  
  // Failed discrimination - determine failure type
  
  // Type II: Stability failure (high variance, non-convergence)
  const stabilityIssues = warnings.filter(w => 
    w.stage === 'evolution' || w.severity === 'high'
  );
  
  if (stabilityIssues.length > 0) {
    return {
      outcome: 'FAILURE',
      type: 'Type II: Stability Failure',
      message: 'Apparent structure is noise-dominated or did not converge',
      epistemic_status: 'Either system lacks τ-closure OR signal-to-noise insufficient',
      evidence: stabilityIssues,
      paper_section: '7.2'
    };
  }
  
  // Type III: Discriminability failure (cannot distinguish from process nulls)
  if (!nulls.level3_passed) {
    return {
      outcome: 'FAILURE',
      type: 'Type III: Discriminability Failure',
      message: 'Cannot distinguish from stochastic process nulls',
      epistemic_status: 'No recursive closure detected at measured resolution',
      discriminability: {
        level1: nulls.level1_passed,
        level2: nulls.level2_passed,
        level3: false
      },
      paper_section: '7.3'
    };
  }
  
  // Type I: Projection failure (phase-randomized null similar to data)
  if (!nulls.level2_passed) {
    return {
      outcome: 'FAILURE',
      type: 'Type I: Projection Failure',
      message: 'Measurement operator P may destroy τ-structure',
      epistemic_status: 'Substrate status uncertain - either τ-closure exists but P inadequate, OR substrate absent',
      suggestion: 'Consider alternative projection or increase sampling resolution',
      paper_section: '7.1'
    };
  }
  
  // Fallback (should not reach)
  return {
    outcome: 'FAILURE',
    type: 'Unclassified Failure',
    message: 'Did not pass discrimination criteria',
    epistemic_status: 'No τ-closure detected',
    paper_section: 'Section 7'
  };
}

/**
 * Compute raw statistics (before correction)
 */
function computeStatistics(tau_data, tau_null_distribution, nullConfig) {
  const n_null = tau_null_distribution.length;
  
  // Compute p-value (one-sided test: data more structured than null)
  const n_more_extreme = tau_null_distribution.filter(tau_null => tau_null <= tau_data).length;
  const pValue = n_more_extreme / n_null;
  
  // Compute effect size (Cohen's d)
  const mean_null = tau_null_distribution.reduce((a, b) => a + b, 0) / n_null;
  const variance_null = tau_null_distribution.reduce((a, b) => a + Math.pow(b - mean_null, 2), 0) / n_null;
  const std_null = Math.sqrt(variance_null);
  
  const cohensD = std_null > 0 ? Math.abs(tau_data - mean_null) / std_null : 0;
  
  return {
    tau_data,
    tau_null_mean: mean_null,
    tau_null_std: std_null,
    pValue,
    cohensD,
    n_null
  };
}

/**
 * Custom error class for pipeline failures
 */
class PipelineError extends Error {
  constructor(stage, message, details = null) {
    super(message);
    this.name = 'PipelineError';
    this.stage = stage;
    this.details = details;
  }
}

/**
 * Field construction (Section 6.1.1)
 * Placeholder - implement based on data type
 */
async function constructField(data, preprocessing) {
  // Implement field construction logic
  return {
    success: true,
    field: data // Placeholder
  };
}

/**
 * Recursive evolution (Section 6.1.2)
 * Placeholder - implement Φ iteration
 */
async function evolveField(field, phi, psi, convergence) {
  // Implement evolution logic
  return {
    converged: true,
    finalField: field, // Placeholder
    iterations: 100
  };
}