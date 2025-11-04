# UNNS Phase VI-VII Integration Guide

## 📦 Deployment Package Contents

```
phase-vi-vii-validation/
├── chamber_xvii_recursive_geometry_coherence.html  (54 KB)
├── chamber_xiv_phi_scale.html                      (61 KB)
├── chamber_cross_validation_dashboard.html         (28 KB)
├── manifest.json                                    (metadata)
├── README.md                                        (user docs)
└── integration-guide.md                             (this file)
```

---

## 🚀 Website Integration Steps

### **Step 1: Upload Chamber Files**

Upload all three HTML files to the library section:

```
/library/operators-xiv-xvii/
  ├── chamber-xvii/
  │   └── index.html  (rename chamber_xvii_recursive_geometry_coherence.html)
  ├── chamber-xiv/
  │   └── index.html  (rename chamber_xiv_phi_scale.html)
  └── dashboard/
      └── index.html  (rename chamber_cross_validation_dashboard.html)
```

**OR** keep original filenames and link directly:

```html
<a href="/library/operators-xiv-xvii/chamber_xvii_recursive_geometry_coherence.html">
  Chamber XVII: Recursive Geometry Coherence Lab
</a>
```

---

### **Step 2: Create Landing Page**

Add a section to the Library index highlighting the Phase VI-VII validation suite:

```html
<section class="library-section">
  <h2>Phase VI-VII: φ-Symmetry Validation Suite</h2>
  <p class="status-badge success">✓ Validation Complete</p>
  
  <div class="chamber-grid">
    <!-- Chamber XVII -->
    <div class="chamber-card">
      <h3>Chamber XVII</h3>
      <p class="chamber-subtitle">Recursive Geometry Coherence</p>
      <div class="chamber-stats">
        <span class="stat">γ★ = 1.60</span>
        <span class="stat success">φ-error: 1.11%</span>
      </div>
      <p class="chamber-desc">
        Validates recursive curvature equations through extended-range 
        sweeps. Features φ-diagnostics, Einstein limit tests, and 
        cross-chamber import.
      </p>
      <a href="/library/operators-xiv-xvii/chamber-xvii/" class="btn-primary">
        Launch Chamber XVII
      </a>
    </div>
    
    <!-- Chamber XIV -->
    <div class="chamber-card">
      <h3>Chamber XIV</h3>
      <p class="chamber-subtitle">Φ-Scale Lab</p>
      <div class="chamber-stats">
        <span class="stat">μ★ = 1.64</span>
        <span class="stat success">φ-error: 1.36%</span>
      </div>
      <p class="chamber-desc">
        Tests spatial scaling operator for φ-resonance through τ-field 
        evolution. Includes μ-diagnostics and fine refinement tools.
      </p>
      <a href="/library/operators-xiv-xvii/chamber-xiv/" class="btn-primary">
        Launch Chamber XIV
      </a>
    </div>
    
    <!-- Phase VII Dashboard -->
    <div class="chamber-card featured">
      <h3>Phase VII Dashboard</h3>
      <p class="chamber-subtitle">Cross-Chamber Validation</p>
      <div class="chamber-stats">
        <span class="stat highlight">γ★/μ★ = 0.976</span>
        <span class="stat highlight">√(γ★·μ★) = 1.62 ≈ φ</span>
      </div>
      <p class="chamber-desc">
        Unified visualization demonstrating dual φ-symmetry across 
        coupling and scaling domains. Import both chamber JSONs for 
        real-time cross-analysis.
      </p>
      <a href="/library/operators-xiv-xvii/dashboard/" class="btn-featured">
        Open Dashboard
      </a>
    </div>
  </div>
  
  <div class="key-findings">
    <h4>Key Validation Results:</h4>
    <ul>
      <li>✓ Both chambers independently converge to φ (< 1.5% error)</li>
      <li>✓ Cross-ratio γ★/μ★ ≈ 1.0 confirms coupling-scale symmetry</li>
      <li>✓ Geometric mean √(γ★·μ★) ≈ φ validates dual-branch model</li>
      <li>✓ All four verification criteria (V1-V4) passed</li>
    </ul>
  </div>
</section>
```

---

### **Step 3: Update Navigation**

Add to main navigation or Operators section:

```html
<nav class="library-nav">
  <a href="#phase-vi-vii">Phase VI-VII Validation</a>
  <!-- existing links -->
</nav>
```

---

### **Step 4: Add Documentation Links**

Link to the technical documentation:

```html
<div class="documentation-links">
  <h4>Documentation & Resources:</h4>
  <ul>
    <li>
      <a href="/docs/operators-xiv-xvi/operator-xvii-validation.pdf">
        Technical Specification: Chamber XVII
      </a>
    </li>
    <li>
      <a href="/docs/operators-xiv-xvi/operator-xiv-phi-scale.pdf">
        Golden Ratio in Recursive Dynamics
      </a>
    </li>
    <li>
      <a href="/library/operators-xiv-xvii/README.md">
        User Guide & Workflow
      </a>
    </li>
    <li>
      <a href="/library/operators-xiv-xvii/manifest.json">
        Metadata & Version Info
      </a>
    </li>
  </ul>
</div>
```

---

### **Step 5: SEO & Metadata**

Add meta tags to chamber pages:

```html
<head>
  <meta name="description" content="UNNS Phase VI-VII: Empirical validation of φ as a dual coupling constant through recursive geometry coherence testing">
  <meta name="keywords" content="UNNS, recursive geometry, golden ratio, phi, validation, quantum gravity">
  <meta property="og:title" content="UNNS Phase VI-VII Validation Suite">
  <meta property="og:description" content="Interactive chambers validating dual φ-symmetry across coupling and scaling domains">
  <meta property="og:image" content="/images/phase-vii-dashboard-preview.png">
  
  <!-- JSON-LD for structured data -->
  <script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "SoftwareApplication",
    "name": "UNNS Phase VI-VII Validation Suite",
    "applicationCategory": "Scientific Simulation",
    "operatingSystem": "Web Browser",
    "description": "Cross-chamber validation of φ-resonance in recursive geometry",
    "version": "1.0.0"
  }
  </script>
</head>
```

---

## 🎨 Styling Recommendations

The chambers use a consistent violet-gold theme. Recommended CSS variables:

```css
:root {
  --chamber-xvii: #8066ff;  /* Violet */
  --chamber-xiv: #ffdd7a;   /* Gold */
  --dashboard: #4ac9e0;     /* Cyan */
  --success: #00d88a;       /* Green */
  --border: rgba(132, 115, 255, 0.25);
}

.chamber-card {
  background: linear-gradient(135deg, rgba(128, 102, 255, 0.06), transparent);
  border: 1px solid var(--border);
  border-radius: 1rem;
  padding: 2rem;
  transition: transform 0.2s;
}

.chamber-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 24px rgba(128, 102, 255, 0.2);
}

.chamber-card.featured {
  background: linear-gradient(135deg, rgba(74, 201, 224, 0.06), transparent);
  border-color: var(--dashboard);
}
```

---

## 📊 Analytics Tracking (Optional)

Track chamber usage:

```javascript
// When chamber loads
gtag('event', 'chamber_open', {
  'chamber_id': 'xvii',
  'version': '0.7.0'
});

// When user runs validation
gtag('event', 'validation_run', {
  'chamber_id': 'xvii',
  'preset': 'phi_zone'
});

// When JSON exported
gtag('event', 'export_data', {
  'chamber_id': 'xvii',
  'gamma_star': 1.60
});
```

---

## 🔄 Update Workflow

When new versions are released:

1. Update `manifest.json` with new version numbers
2. Replace HTML files in library directory
3. Update changelog in README.md
4. Clear CDN cache if applicable
5. Announce update on homepage/blog

---

## 🧪 Testing Checklist

Before going live:

- [ ] All three chamber files load correctly
- [ ] Dashboard accepts both XIV and XVII JSONs
- [ ] Export functionality works in all chambers
- [ ] Mobile responsive (test on 768px, 414px)
- [ ] Cross-browser compatibility (Chrome, Firefox, Safari, Edge)
- [ ] All links in documentation work
- [ ] Metadata/manifest.json accessible
- [ ] 404 pages handled gracefully

---

## 🔐 Security Considerations

- All chambers are **client-side only** (no server communication)
- No API keys or credentials embedded
- File upload uses browser FileReader API (local only)
- No external dependencies or CDN calls
- Safe for use in secured/airgapped environments

---

## 📞 Support & Maintenance

**Issue Reporting:**
- GitHub Issues (if repository public)
- Email: contact@unns.tech
- In-site feedback form

**Version Control:**
- Keep manifest.json as source of truth
- Tag releases: `v1.0.0`, `v1.1.0`, etc.
- Archive old versions in `/library/archive/`

**Backup:**
- Keep copies of all chamber HTMLs
- Export sample JSONs for testing
- Document any custom modifications

---

## ✅ Final Deployment Command

```bash
# Navigate to library directory
cd /path/to/unns.tech/library/

# Create operators directory
mkdir -p operators-xiv-xvii/{chamber-xvii,chamber-xiv,dashboard}

# Copy files
cp chamber_xvii_recursive_geometry_coherence.html operators-xiv-xvii/chamber-xvii/index.html
cp chamber_xiv_phi_scale.html operators-xiv-xvii/chamber-xiv/index.html
cp chamber_cross_validation_dashboard.html operators-xiv-xvii/dashboard/index.html

# Copy metadata
cp manifest.json operators-xiv-xvii/
cp README.md operators-xiv-xvii/
cp integration-guide.md operators-xiv-xvii/

# Set permissions
chmod 644 operators-xiv-xvii/**/*.html
chmod 644 operators-xiv-xvii/*.{json,md}

# Test locally
python3 -m http.server 8000
# Visit: http://localhost:8000/operators-xiv-xvii/dashboard/

# Deploy to production
# (use your deployment pipeline)
```

---

## 🎉 Launch Announcement Template

**Blog Post / News Section:**

```markdown
# Phase VI-VII Validation Complete: φ-Symmetry Confirmed

We're excited to announce the completion of UNNS Phase VI-VII validation, 
demonstrating empirical evidence for φ as a dual coupling constant across 
recursive geometry domains.

## Key Results
- **Chamber XVII** (Recursive Coupling): γ★ = 1.60, φ-error = 1.11%
- **Chamber XIV** (Spatial Scaling): μ★ = 1.64, φ-error = 1.36%
- **Cross-Validation**: √(γ★·μ★) = 1.62 ≈ φ (0.12% error)

## Interactive Tools Now Live
Explore the validation suite:
- [Chamber XVII →](/library/operators-xiv-xvii/chamber-xvii/)
- [Chamber XIV →](/library/operators-xiv-xvii/chamber-xiv/)
- [Phase VII Dashboard →](/library/operators-xiv-xvii/dashboard/)

All chambers are production-ready, self-contained, and require no 
installation. Simply open in your browser and start validating!

[Read full technical report →](/docs/phase-vii-validation-report.pdf)
```

---

**Status:** Ready for deployment ✅  
**Last Updated:** 2025-11-03  
**Contact:** UNNS Lab
