import altair as alt
from vega_datasets import data as vega_data

movies_url = vega_data.movies.url

# ── Shared encodings ─────────────────────────────────────────────────────────
x_enc = alt.X('Rotten_Tomatoes_Rating:Q',
               bin=alt.BinParams(maxbins=20),
               title='Rotten Tomatoes Rating')
y_enc = alt.Y('IMDB_Rating:Q',
               bin=alt.BinParams(maxbins=20),
               title='IMDB Rating')
tooltip = [
    alt.Tooltip('Rotten_Tomatoes_Rating:Q', bin=alt.BinParams(maxbins=20), title='RT Rating (bin)'),
    alt.Tooltip('IMDB_Rating:Q',            bin=alt.BinParams(maxbins=20), title='IMDB Rating (bin)'),
    alt.Tooltip('count():Q',                title='Number of Films'),
]

base = alt.Chart(movies_url).mark_rect(
    stroke='white',
    strokeWidth=0.5
).encode(
    x=x_enc,
    y=y_enc,
    tooltip=tooltip
).properties(width=300, height=300)

# ── Plot 1: Diverging palette PRGn (colorblind-safe) ─────────────────────────
# Exact 5-step hex stops from https://colorbrewer2.org/#type=diverging&scheme=PRGn&n=5
# Purple–Green is colorblind-safe: the two hues differ strongly in luminance.
# domainMid=0 pins the neutral colour (#f7f7f7) to zero counts, so even a
# single film creates a visible colour shift — producing the "sharper transitions"
# requested by the homework.
prgn5 = ['#762a83', '#af8dc3', '#f7f7f7', '#7fbf7b', '#1b7837']
plot_diverging = base.encode(
    alt.Color('count():Q',
               scale=alt.Scale(range=prgn5, domainMid=0),
               legend=alt.Legend(title='Number of Films'))
).properties(
    title=alt.TitleParams(
        text='Diverging Palette (PRGn)',
        subtitle='Purple = sparse  |  Green = dense'
    )
)

# ── Plot 2: Sequential palette Blues, low values = white, cell outlines ───────
# Explicit stops: white for the lowest count, dark blue for the highest.
# Using range= makes the direction unambiguous regardless of Altair/Vega version.
# Single-hue luminance ramp → universally colorblind-safe.
blues = ['#ffffff', '#deebf7', '#9ecae1', '#3182bd', '#08519c']
plot_sequential = base.encode(
    alt.Color('count():Q',
               scale=alt.Scale(range=blues),
               legend=alt.Legend(title='Number of Films'))
).properties(
    title=alt.TitleParams(
        text='Sequential Palette (Blues)',
        subtitle='White = sparse  |  Dark blue = dense'
    )
)

# ── Horizontal concatenation ──────────────────────────────────────────────────
combined = alt.hconcat(
    plot_diverging,
    plot_sequential
).properties(
    title=alt.TitleParams(
        text='Movie Ratings Heatmap – Rotten Tomatoes vs. IMDB',
        subtitle='Hover over any cell to see exact values. Both palettes are colorblind-safe.',
        anchor='middle',
        fontSize=16,
        subtitleFontSize=12
    )
).configure_view(
    strokeWidth=0
).configure_axis(
    labelFontSize=11,
    titleFontSize=12
).configure_legend(
    labelFontSize=10,
    titleFontSize=11
)

combined
