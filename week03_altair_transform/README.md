# Week 03 — Color Scales & 2D Histograms (Heatmaps)

## 🎯 Task

Adapted the 2D histogram / heatmap from the *Histograms* section of the course using two colorblind-safe palettes, then combined both into a single horizontally concatenated view:

1. **Diverging palette (PRGn, n=5)** — sharper transitions via [ColorBrewer PRGn](https://colorbrewer2.org/#type=diverging&scheme=PRGn&n=5), purple = sparse, green = dense.
2. **Sequential palette (Blues)** — same heatmap recolored with a white-to-dark-blue sequential ramp, low counts shown in white, cell outlines added.
3. Both charts concatenated horizontally (`alt.hconcat`) with tooltips showing bin ranges and exact film counts.

## 📊 Dataset

`vega_datasets` → `movies.json` (3 201 films), comparing `Rotten_Tomatoes_Rating` vs `IMDB_Rating`, binned into 20×20 cells per axis.

## 🎨 Design notes

- **PRGn diverging**: exact 5-step hex stops from ColorBrewer, `domainMid=0` pins the neutral color to zero counts so even a single film produces a visible shift.
- **Blues sequential**: explicit `range=` stops (white → dark blue) to avoid ambiguity across Altair/Vega versions; cell outlines (`stroke='white'`) added for readability.
- Both palettes confirmed colorblind-safe (Wong 2011 / ColorBrewer guidance) — PRGn relies on hue *and* luminance contrast, Blues relies purely on luminance, covering all common forms of color vision deficiency.

## 📁 Files

- `homework/homework3.py` — Altair chart construction (Python)
- `submission/homework3.html` — self-contained interactive HTML export submitted to instructor

## 🖼️ Preview

Open `submission/homework3.html` in a browser to interact with both heatmaps (hover for tooltips).
