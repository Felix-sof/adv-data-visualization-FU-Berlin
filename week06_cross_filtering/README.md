# Week 06 – Interaction (Linked Brushing & Cross-Filtering)

## Task Description (from the course notebook)

> Adapt the last chart in 'Binding Selections to Multiple Inputs' for this
> homework by preserving the rating option but by creating a SPLOM chart to
> show the Movie Genres.
>
> Include linking and brushing functionalities as seen later on in this
> practical. Check that all functionalities work as intended. Add a main
> title for the main chart and center the selection of the Rating
> underneath.
>
> Export as a single HTML file.

## What this does

A "Movie Ratings Explorer" dashboard over the `movies` dataset, with three
coordinated views driven by three shared selections:

| Selection | Type | Behavior |
|---|---|---|
| `mpaa_filter` | `selection_point` bound to a **radio group** | preserves the "rating option" from the multi-input binding example |
| `splom_brush` | `selection_interval`, `resolve='global'` | one active brush shared across every SPLOM cell (cross-filtering) |
| `genre_highlight` | `selection_point` bound to the **legend** | click a genre to highlight just that genre |

| View | Role |
|---|---|
| Selected-count label | live count of films matching all three filters (`transform_aggregate` after three chained `transform_filter`s) |
| SPLOM (`IMDB_Rating` · `Rotten_Tomatoes_Rating` · `IMDB_Votes` · `Worldwide_Gross`) | brushable, colored by `Major_Genre` |
| Genre bar chart | grey background layer = MPAA-filtered totals; colored foreground layer = brush + MPAA + legend filtered counts |

### Functionality check

- **Brushing** — dragging a rectangle in any SPLOM cell greys out
  non-selected points in every other cell (global resolve) and updates the
  genre bar chart and the counter.
- **MPAA radio filter** — switching the rating narrows every view.
- **Legend click-to-highlight** — clicking a genre in the SPLOM legend
  raises its opacity and filters the foreground bar layer + counter to it.
- All three combine correctly: the bar chart's foreground layer and the
  counter filter on all three selections together.

### Layout

- A centered main title (`anchor='middle'`) on the whole dashboard.
- The MPAA radio buttons are centered underneath the chart via a small CSS
  rule injected into the exported HTML's `<head>` (`form.vega-bindings {
  display:flex; justify-content:center; }`) — Vega-Lite itself doesn't
  expose a "center this binding" option, so this is done as a page-level
  style tweak at export time.

## Data

`movies.json` from
[vega-datasets](https://cdn.jsdelivr.net/npm/vega-datasets@1/data/movies.json).

## Files

- `homework/homework6_movie_ratings_explorer.py` — the dashboard code (converted from the notebook below)
- `homework/homework6_movie_ratings_explorer.ipynb` — the original notebook, run in Jupyter Lab
- `submission/homework6_movie_ratings_explorer.html` — single-file HTML export, submitted to the instructor

## Running it

```bash
python homework6_movie_ratings_explorer.py
```

or open `homework6_movie_ratings_explorer.ipynb` in Jupyter Lab and run all
cells. Either way, running it writes
`homework6_movie_ratings_explorer.html` next to the script.
