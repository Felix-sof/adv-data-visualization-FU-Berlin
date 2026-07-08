# Homework 8 — Heat & Mortality in Germany

Exploratory data analysis on the relationship between weekly Berlin temperature and weekly all-cause mortality in Germany (2015–2024), built with pandas and Altair.

**Research question:** Is there a relationship between weekly temperature in Berlin and weekly all-cause mortality in Germany?

## Data sources

| Dataset | Source | Access |
|---|---|---|
| Weekly all-cause mortality, Germany (2015–2024) | [World Mortality Dataset](https://github.com/akarlinsky/world_mortality) (Karlinsky & Kobak, 2021, *eLife*) | `pd.read_csv()` on raw CSV |
| Daily temperature, Berlin (2015–2024, ERA5 reanalysis) | [Open-Meteo Historical Weather API](https://open-meteo.com) | `requests.get()`, no API key required |

Temperature is aggregated to weekly values (mean / max / min) and merged with the mortality series by ISO week into a single working dataset, `data_heat`.

## What's in this analysis

- **Correlation matrix** — Pearson correlation between `deaths`, `temp_mean`, `temp_max`, `temp_min`, including an upper-triangle-only variant.
- **Mutual information matrix** — pairwise mutual information across the same variables, to check for non-linear relationships that Pearson correlation could miss.
- **Parallel coordinates chart** — one line per week across `temp_mean`, `temp_max`, `temp_min`, `deaths`, colored by season; shown raw, standardized, min-max normalized, with an alternate axis ordering, and with hover-based season filtering.
- **Scatter plot matrix (SPLOM)** — pairwise scatter plots of the four numeric variables colored by season, with interactive linked brushing, plus a manually-built lower-triangle-only version.
- **Final dashboard** — the correlation matrix, mutual information matrix, standardized parallel coordinates chart, and brushed SPLOM combined into one multi-visualization HTML export.

## Repo structure

- `homework/homework8_heat_mortality.py` — self-contained analysis script (converted from the original notebook)
- `submission/homework8_heat_mortality.html` — exported multi-chart HTML dashboard

## Notes on scope

This is a classroom EDA exercise, not a peer-reviewed causal study. Mortality has several drivers (flu season, COVID-19, demographic aging, etc.) — temperature is only one factor, and weekly national aggregates can't capture the local, age-specific effects that real heat-mortality research relies on. Correlations here are descriptive, not causal.
