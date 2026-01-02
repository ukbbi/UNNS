/**
 * Chamber XXXII — Type IV Failure Detector
 * Implements Section 7.4 from Observability Paper
 * 
 * CRITICAL: Detects parameter tuning / p-hacking
 * - Tracks run history across sessions
 * - Flags excessive parameter changes
 * - Detects correlation between tuning and success
 * - Cannot be disabled
 * 
 * @version 1.0.0
 * @phase Phase 1 (L5-Ready: Basic)
 */

import { HistoryStorage } from './HistoryStorage.js';

export class TypeIVDetector {
  /**
   * @param {Storage} storageBackend - localStorage, indexedDB, or server
   * @param {Object} config - Detection thresholds
   */
  constructor(storageBackend, config = {}) {
    this.storage = new HistoryStorage(storageBackend);
    
    // Detection thresholds (from paper Section 7.4)
    this.thresholds = {
      max_param_changes: config.max_param_changes || 3,
      correlation_threshold: config.correlation_threshold || 0.7,
      min_runs_for_correlation: config.min_runs_for_correlation || 5,
      cross_dataset_tolerance: config.cross_dataset_tolerance || 0.2
    };
    
    // Load history
    this.sessionHistory = this.storage.loadHistory();
    
    console.log(`[TypeIVDetector] Loaded ${this.sessionHistory.length} historical runs`);
  }
  
  /**
   * Record a new run for Type IV analysis
   * 
   * @param {Object} config - {phi, psi, collapse, metric, thresholds}
   * @param {Object} outcome - {verdict, pValues, effectSize, passed}
   * @param {string} datasetId - Hash of input data
   * @returns {Object} - Type IV analysis result
   */
  recordRun(config, outcome, datasetId) {
    const entry = {
      timestamp: Date.now(),
      configHash: this._hashConfig(config),
      config: this._extractRelevantConfig(config),
      outcome: {
        verdict: outcome.verdict,
        passed: outcome.passed || false,
        pValue: outcome.pValue || 1.0,
        effectSize: outcome.effectSize || 0
      },
      datasetId: datasetId
    };
    
    // Add to history
    this.sessionHistory.push(entry);
    this.storage.saveHistory(this.sessionHistory);
    
    // Analyze for Type IV patterns
    const analysis = this._analyzeHistory();
    
    // Log results
    if (analysis.triggered) {
      console.warn('[TypeIVDetector] ⚠️ TYPE IV FAILURE DETECTED');
      console.warn('Evidence:', analysis.triggers);
    }
    
    return analysis;
  }
  
  /**
   * Main Type IV detection logic
   * 
   * Tests for three patterns:
   * 1. Parameter drift (excessive config changes)
   * 2. P-hacking (tuning correlates with p-value improvement)
   * 3. Dataset selectivity (works on some datasets, fails on others)
   */
  _analyzeHistory() {
    const triggers = [];
    
    // PATTERN 1: Parameter drift
    const driftTrigger = this._detectParameterDrift();
    if (driftTrigger) {
      triggers.push(driftTrigger);
    }
    
    // PATTERN 2: P-hacking (requires sufficient history)
    if (this.sessionHistory.length >= this.thresholds.min_runs_for_correlation) {
      const phackingTrigger = this._detectPHacking();
      if (phackingTrigger) {
        triggers.push(phackingTrigger);
      }
    }
    
    // PATTERN 3: Dataset selectivity (requires multiple datasets)
    const datasets = new Set(this.sessionHistory.map(r => r.datasetId));
    if (datasets.size > 1) {
      const selectivityTrigger = this._detectDatasetSelectivity();
      if (selectivityTrigger) {
        triggers.push(selectivityTrigger);
      }
    }
    
    // Generate verdict
    return {
      triggered: triggers.length > 0,
      triggers: triggers,
      recommendation: this._generateRecommendation(triggers),
      evidence: this._compileEvidence(triggers),
      severity: this._assessSeverity(triggers)
    };
  }
  
  /**
   * PATTERN 1: Detect excessive parameter changes
   */
  _detectParameterDrift() {
    // Group by dataset
    const byDataset = this._groupByDataset(this.sessionHistory);
    
    for (const [datasetId, runs] of Object.entries(byDataset)) {
      const uniqueConfigs = new Set(runs.map(r => r.configHash)).size;
      
      if (uniqueConfigs > this.thresholds.max_param_changes) {
        return {
          type: 'parameter_drift',
          datasetId,
          uniqueConfigs,
          threshold: this.thresholds.max_param_changes,
          severity: uniqueConfigs > 2 * this.thresholds.max_param_changes ? 'severe' : 'moderate',
          message: `${uniqueConfigs} different operator configs tried on same dataset (threshold: ${this.thresholds.max_param_changes})`,
          evidence: {
            configs: runs.map(r => ({
              timestamp: r.timestamp,
              hash: r.configHash,
              passed: r.outcome.passed
            }))
          }
        };
      }
    }
    
    return null;
  }
  
  /**
   * PATTERN 2: Detect p-hacking (correlation between parameter changes and p-value improvement)
   */
  _detectPHacking() {
    if (this.sessionHistory.length < 2) return null;
    
    // Compute config change magnitude over time
    const configChanges = [];
    const pValueChanges = [];
    
    for (let i = 1; i < this.sessionHistory.length; i++) {
      const prev = this.sessionHistory[i - 1];
      const curr = this.sessionHistory[i];
      
      // Config changed?
      const configDelta = prev.configHash !== curr.configHash ? 1 : 0;
      configChanges.push(configDelta);
      
      // P-value improved?
      const pDelta = curr.outcome.pValue - prev.outcome.pValue;
      pValueChanges.push(pDelta);
    }
    
    // Compute correlation
    const correlation = this._pearsonCorrelation(configChanges, pValueChanges);
    
    // P-hacking detected if:
    // - Strong negative correlation (config changes → lower p-values)
    if (Math.abs(correlation) > this.thresholds.correlation_threshold) {
      return {
        type: 'p_hacking',
        correlation: correlation,
        threshold: this.thresholds.correlation_threshold,
        severity: 'critical',
        message: `Parameter tuning strongly correlates with p-value changes (r = ${correlation.toFixed(3)})`,
        evidence: {
          n_samples: configChanges.length,
          configChanges,
          pValueChanges,
          interpretation: correlation < 0 
            ? 'Config changes → lower p-values (likely p-hacking)'
            : 'Config changes → higher p-values (unusual)'
        }
      };
    }
    
    return null;
  }
  
  /**
   * PATTERN 3: Detect dataset selectivity
   */
  _detectDatasetSelectivity() {
    const byDataset = this._groupByDataset(this.sessionHistory);
    const datasets = Object.keys(byDataset);
    
    if (datasets.length < 2) return null;
    
    // Build config × dataset performance matrix
    const configPerformance = {};
    
    for (const [datasetId, runs] of Object.entries(byDataset)) {
      for (const run of runs) {
        if (!configPerformance[run.configHash]) {
          configPerformance[run.configHash] = {};
        }
        
        configPerformance[run.configHash][datasetId] = run.outcome.passed;
      }
    }
    
    // Find configs with inconsistent performance across datasets
    const inconsistentConfigs = [];
    
    for (const [configHash, performance] of Object.entries(configPerformance)) {
      const results = Object.values(performance);
      
      if (results.includes(true) && results.includes(false)) {
        inconsistentConfigs.push({
          configHash,
          performance,
          successRate: results.filter(r => r).length / results.length
        });
      }
    }
    
    if (inconsistentConfigs.length > 0) {
      return {
        type: 'dataset_selectivity',
        severity: 'moderate',
        inconsistentConfigs: inconsistentConfigs.length,
        message: `Operator succeeds on some datasets but fails on others (${inconsistentConfigs.length} inconsistent configs)`,
        evidence: {
          configs: inconsistentConfigs,
          interpretation: 'Operator may be dataset-specific (non-universal τ-signature)'
        }
      };
    }
    
    return null;
  }
  
  /**
   * Generate recommendation based on triggers
   */
  _generateRecommendation(triggers) {
    if (triggers.length === 0) {
      return null;
    }
    
    // Priority order: p-hacking > drift > selectivity
    if (triggers.some(t => t.type === 'p_hacking')) {
      return {
        action: 'RESTART',
        message: 'CRITICAL: P-hacking detected. Results invalid. Restart with pre-registered Φ definition.',
        severity: 'critical'
      };
    }
    
    if (triggers.some(t => t.type === 'parameter_drift')) {
      return {
        action: 'FREEZE_PHI',
        message: 'Excessive parameter tuning detected. FREEZE Φ definition before further runs.',
        severity: 'severe'
      };
    }
    
    if (triggers.some(t => t.type === 'dataset_selectivity')) {
      return {
        action: 'CLASSIFY',
        message: 'Method appears dataset-specific. Either (1) multiple τ-closure classes exist, or (2) operator not universal.',
        severity: 'moderate'
      };
    }
    
    return {
      action: 'REVIEW',
      message: 'Type IV patterns detected. Review operator definition.',
      severity: 'moderate'
    };
  }
  
  /**
   * Compile evidence for export
   */
  _compileEvidence(triggers) {
    return {
      n_runs: this.sessionHistory.length,
      n_datasets: new Set(this.sessionHistory.map(r => r.datasetId)).size,
      n_configs: new Set(this.sessionHistory.map(r => r.configHash)).size,
      triggers: triggers,
      full_history: this.sessionHistory.map(r => ({
        timestamp: new Date(r.timestamp).toISOString(),
        configHash: r.configHash,
        datasetId: r.datasetId,
        passed: r.outcome.passed,
        pValue: r.outcome.pValue
      }))
    };
  }
  
  /**
   * Assess overall severity
   */
  _assessSeverity(triggers) {
    if (triggers.some(t => t.severity === 'critical')) return 'critical';
    if (triggers.some(t => t.severity === 'severe')) return 'severe';
    if (triggers.some(t => t.severity === 'moderate')) return 'moderate';
    return 'low';
  }
  
  // ========================================
  // UTILITIES
  // ========================================
  
  _groupByDataset(history) {
    const grouped = {};
    for (const run of history) {
      if (!grouped[run.datasetId]) {
        grouped[run.datasetId] = [];
      }
      grouped[run.datasetId].push(run);
    }
    return grouped;
  }
  
  _hashConfig(config) {
    // Extract deterministic fingerprint of config
    const relevant = this._extractRelevantConfig(config);
    const str = JSON.stringify(relevant);
    
    // Simple hash
    let hash = 0;
    for (let i = 0; i < str.length; i++) {
      const char = str.charCodeAt(i);
      hash = ((hash << 5) - hash) + char;
      hash = hash & hash;
    }
    
    return hash.toString(16);
  }
  
  _extractRelevantConfig(config) {
    return {
      phi: config.phi?.type || config.phi,
      psi: config.psi,
      collapse: config.collapse,
      metric: config.metric,
      thresholds: config.thresholds
    };
  }
  
  _pearsonCorrelation(x, y) {
    if (x.length !== y.length || x.length === 0) return 0;
    
    const n = x.length;
    const mean_x = x.reduce((a, b) => a + b, 0) / n;
    const mean_y = y.reduce((a, b) => a + b, 0) / n;
    
    let num = 0;
    let den_x = 0;
    let den_y = 0;
    
    for (let i = 0; i < n; i++) {
      const dx = x[i] - mean_x;
      const dy = y[i] - mean_y;
      num += dx * dy;
      den_x += dx * dx;
      den_y += dy * dy;
    }
    
    if (den_x === 0 || den_y === 0) return 0;
    
    return num / Math.sqrt(den_x * den_y);
  }
  
  /**
   * Clear history (requires confirmation)
   */
  clearHistory(force = false) {
    if (!force) {
      throw new Error('clearHistory() requires force=true confirmation. This deletes all run history.');
    }
    
    this.sessionHistory = [];
    this.storage.saveHistory([]);
    
    console.warn('[TypeIVDetector] History cleared');
  }
  
  /**
   * Export for debugging/auditing
   */
  exportHistory() {
    return {
      version: '1.0.0',
      timestamp: Date.now(),
      n_runs: this.sessionHistory.length,
      history: this.sessionHistory,
      thresholds: this.thresholds
    };
  }
}