# Week 04 — Scales, Axes & Legends: Color Scheme Comparison

## 🎯 Task

Adapted the Penicillin MIC heatmap into a **small-multiples** layout comparing four Vega color schemes — `greys`, `viridis`, `rainbow`, `yelloworangered` — on the identical log-scaled domain, then evaluated each for color-blind accessibility and stated a final preference.

1. Same data, same log-scale domain across all four panels — only the color scheme changes.
2. Color chosen to reflect concentration semantics (natural yellow = effective/diluted vs. red = high dose/resistant), noting `1000 µg/ml` (resistant) is far larger than `0.0001 µg/ml` (effective).
3. Accessibility checked via [Coblis](https://www.color-blindness.com/coblis-color-blindness-simulator/) against Deuteranopia, Protanopia, Tritanopia, and Achromatopsia.
4. Exported as a single self-contained HTML file with tooltips.

## 📊 Dataset

`vega_datasets` → `burtin.json` — antibiotic MIC (minimum inhibitory concentration) values for 16 bacterial strains across Penicillin, Streptomycin, and Neomycin, with Gram staining classification.

## 🎨 Findings & preference

| Scheme | Accessibility | Notes |
|---|---|---|
| `greys` | ★ Most accessible | Unaffected by all 4 deficiencies, but no semantic concentration mapping |
| `viridis` | ★ Excellent | Perceptually uniform, robust under deutan/protan, slight tritan shift |
| `rainbow` | ✗ Least accessible | Red/green collapse under deutan/protan, non-monotone luminance → false ordering |
| `yelloworangered` | △ Good, caution w/ protanopia | Warm ramp matches natural penicillin semantics (yellow=diluted, red=concentrated) |

**Preference: `yelloworangered`**, with `viridis` as the accessibility fallback — chosen for its direct semantic mapping to the data (matches natural warning conventions), while acknowledging its weakness under protanopia is mitigated by tooltips exposing exact values.

## 📁 Files

- `homework/Exercise04_Sanberk.py` — full Altair exercise walkthrough + small-multiples construction (Python)
- `submission/homework4_antibiotic_color_schemes.html` — self-contained interactive HTML export submitted to instructor

## 🖼️ Preview

Open `submission/homework4_antibiotic_color_schemes.html` in a browser to interact with all four heatmaps and view the accessibility breakdown.
