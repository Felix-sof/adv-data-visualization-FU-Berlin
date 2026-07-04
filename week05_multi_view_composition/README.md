# Week 05 – Multi-View Composition

## Task Description (from the course notebook)

> Adapt the last chart to add a dropdown menu for the different cities in the data.
> Consider another color for the SPLOM base chart to easily differentiate the default
> color from the rain categorical encoding in the facet-based composite chart.
> Check for accessibility using Coblis and adjust colors accordingly.
> Export as a single HTML file.

## What this does

An interactive weather dashboard comparing **Seattle** and **New York**,
built from three coordinated views:

| View | Composition operator |
|---|---|
| Scatter Plot Matrix (`temp_max` · `precipitation` · `wind`) | `repeat` (row × column) |
| Monthly average + overall mean rule, per field | `repeat` + `layer` |
| Temperature distribution by weather type | `facet` |
| All three combined | `vconcat` + `hconcat` |

### Interactivity

- **City dropdown** — `alt.selection_point(bind=alt.binding_select(...))`
  replaces a hard-coded `location == "Seattle"` filter. The dropdown is
  compiled directly into the Vega-Lite spec, so it keeps working after
  exporting to a static HTML file — no running Python kernel required.
- **Click-to-isolate legend** — clicking a weather type in the legend
  (`alt.selection_point(bind='legend')`) fades out the other categories, so
  a category can be isolated by its text label, not only by its color.
- **Tooltips** on every chart, showing exact numeric values on hover.
- **Pan / zoom** on the SPLOM (`alt.selection_interval(bind='scales')`).

### Accessibility

All categorical colors use the **Wong (2011) / Okabe–Ito** colorblind-safe
palette:

| Element | Color | Wong name |
|---|---|---|
| SPLOM points | `#D55E00` | vermillion |
| drizzle | `#56B4E9` | sky blue |
| fog | `#999999` | grey |
| rain | `#0072B2` | blue |
| snow | `#CC79A7` | reddish purple |
| sun | `#E69F00` | orange |
| mean rule (dashed) | `#D55E00` | vermillion |

Verified with [Coblis](https://www.color-blindness.com/coblis-color-blindness-simulator/)
under protanopia, deuteranopia, and tritanopia — the SPLOM's vermillion
stays clearly separable from the facet's blue `rain` category in every
simulation. On top of color, the tooltips and click-to-isolate legend give
two color-independent ways to read the data.

### Dark theme

A custom Altair theme (`dark_github`) is registered and enabled globally, so
every chart renders on a dark background (`#0d1117`) with light text
(`#e6edf3`). At export time, the same dark background is also applied to
the surrounding HTML page's `<body>`, so the whole exported file — not just
the charts — is dark.

## Data

Seattle / New York weather dataset (`location, date, precipitation,
temp_max, temp_min, wind, weather`), loaded directly by URL so Vega-Lite
fetches it client-side:
[vega-datasets/weather.csv](https://vega.github.io/vega-datasets/data/weather.csv).

## Files

- `homework/homework5_weather_dashboard.py` — the dashboard code (converted from the notebook below)
- `homework/homework5_weather_dashboard.ipynb` — the original interactive notebook, run in Jupyter Lab
- `submission/homework5_weather_dashboard.html` — single-file HTML export, submitted to the instructor

## Running it

```bash
python homework5_weather_dashboard.py
```

or open `homework5_weather_dashboard.ipynb` in Jupyter Lab and run all
cells. Either way, running it writes `homework5_weather_dashboard.html` —
the finished, self-contained, interactive dashboard — next to the script.
