# Week 07 – Geographic Projections (Small Multiples)

## Task Description

> Adapt the following code of the small multiple chart to show the
> unemployment rates and change the different specific projection types.
>
> Observe changes and appreciate the distances among regions. Consider your
> favorite specific projection type. Add a main title for the main chart
> and explain your decision.
>
> Export as a single HTML file.

The starting point was a `facet`-based small multiple of US income share by
group, using a single `albersUsa` projection. This homework instead builds
**four separate maps**, one per projection, so the *same* variable
(unemployment rate) can be compared side by side across projections —
`facet` only repeats by a data field, not by a chart property like
`projection.type`, so each map is built individually with a `make_map()`
function and combined with `vconcat`/`hconcat`.

## What this does

| Projection | Property |
|---|---|
| `albersUsa` | equal-area, purpose-built for the US; repositions Alaska & Hawaii into insets |
| `albers` | equal-area conic, but without the US-specific repositioning |
| `conicEqualArea` | generic equal-area conic |
| `conicConformal` | conformal (preserves local shape/angles), at the cost of area distortion |

All four maps encode US county-level **unemployment rate** with the same
`viridis` color scale (domain fixed to `[0, 0.25]` so colors are directly
comparable across panels), and share:

- a **hover highlight** (`selection_point(on='mouseover')`) that outlines
  the hovered county in black and raises it to full opacity,
- a **tooltip** showing the exact rate,
- independent **pan/zoom** per map (`.interactive()`), and
- Alaska, Hawaii, and Puerto Rico excluded from all four, so every
  projection frames only the 48 contiguous states — otherwise the
  non-`albersUsa` projections stretch Alaska/Hawaii/PR into the same plane
  as the mainland and the comparison becomes meaningless.

## Favorite projection & why

**Albers USA.** It's the only one of the four purpose-built for this exact
map: it preserves area (so color-by-rate comparisons across counties of
different size stay honest) and repositions Alaska and Hawaii into compact
insets instead of stretching the projection to cover their true geographic
location, which is what happens to `albers` and both conic projections
here — since they aren't given the US-specific insets, the underlying
geometry would either clip those states out or badly distort the
contiguous states to fit them in. Keeping the comparison limited to the
48 contiguous states makes `albersUsa` and plain `albers` look similar,
but `albersUsa`'s insets are exactly why it's the standard choice for US
choropleths outside this exercise.

This is stated as the dashboard's subtitle as well.

## Data

- `us-10m.json` (counties topology) and `unemployment.tsv`, both from
  [vega-datasets](https://cdn.jsdelivr.net/npm/vega-datasets@v1.29.0/).

## Files

- `homework/homework7_unemployment_projections.py` — the chart code (converted from the notebook below)
- `homework/homework7_unemployment_projections.ipynb` — the original notebook, run in Jupyter Lab
- `submission/Homework7_Unemployment_Projections_Interactive.html` — single-file HTML export, submitted to the instructor

## Running it

```bash
python homework7_unemployment_projections.py
```

or open `homework7_unemployment_projections.ipynb` in Jupyter Lab and run
the cell. Either way, running it writes
`Homework7_Unemployment_Projections_Interactive.html` next to the script.
