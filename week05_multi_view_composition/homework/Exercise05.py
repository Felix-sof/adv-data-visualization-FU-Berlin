# %% [markdown]
# # Homework 5 – Multi-View Composition Dashboard (v2)
# 
# **Task** (from the course notebook):
# 
# > Adapt the last chart to add a dropdown menu for the different cities in the data.
# > Consider another color for the SPLOM base chart to easily differentiate the default
# > color from the rain categorical encoding in the facet-based composite chart.
# > Check for accessibility using Coblis and adjust colors accordingly.
# > Export as a single HTML file.
# 
# **v2 adds, on top of the base requirement:**
# 
# 1. **Dark theme** — applied globally via an Altair theme, so every chart (and
#    the exported HTML page itself) uses a dark background.
# 2. **Click-to-isolate legend** — clicking a weather type in the legend fades
#    out the other categories, so users don't have to rely purely on
#    distinguishing colors at a glance.
# 3. **Tooltips everywhere** — exact numeric values on hover, a second,
#    color-independent way to read the data.
# 4. **Pan / zoom on the SPLOM** — scroll or drag to explore dense regions.
# 5. Same interactive **city dropdown** and **colorblind-safe Wong palette**
#    as before.

# %% [code cell 1]
import pandas as pd
import altair as alt

# %% [markdown]
# ## Load data

# %% [code cell 2]
weather = 'https://vega.github.io/vega-datasets/data/weather.csv'

df = pd.read_csv(weather)
df.head()

# %% [markdown]
# ## Colors — Wong (2011) / Okabe–Ito colorblind-safe palette
# 
# Same palette as before. The SPLOM keeps **vermillion**, clearly distinct
# from the facet histogram's **blue** `rain` category — checked with
# [Coblis](https://www.color-blindness.com/coblis-color-blindness-simulator/)
# under protanopia, deuteranopia, and tritanopia.

# %% [code cell 3]
WONG = {
    'orange':          '#E69F00',
    'sky_blue':        '#56B4E9',
    'bluish_green':    '#009E73',
    'yellow':          '#F0E442',
    'blue':            '#0072B2',
    'vermillion':      '#D55E00',
    'reddish_purple':  '#CC79A7',
    'grey':            '#999999',
}

weather_colors = alt.Scale(
    domain=['drizzle', 'fog', 'rain', 'snow', 'sun'],
    range=[
        WONG['sky_blue'],       # drizzle
        WONG['grey'],           # fog
        WONG['blue'],           # rain
        WONG['reddish_purple'], # snow
        WONG['orange'],         # sun
    ]
)

SPLOM_COLOR = WONG['vermillion']

# %% [markdown]
# ## Dark theme
# 
# Registered as a reusable Altair theme so it applies to every chart in this
# notebook — and gets baked into the exported HTML's Vega-Lite spec, so the
# charts stay dark even after export. (We'll separately style the HTML page's
# `<body>` background at export time, since that's outside the chart spec.)

# %% [code cell 4]
BG = '#0d1117'
PANEL = '#161b22'
BORDER = '#30363d'
TEXT = '#e6edf3'
MUTED = '#8b949e'
FONT = 'Courier New, Courier, monospace'

def dark_theme():
    return {
        'config': {
            'background': BG,
            'view': {'stroke': 'transparent', 'fill': PANEL},
            'title': {'color': TEXT, 'font': FONT, 'fontSize': 15, 'anchor': 'start'},
            'axis': {
                'domainColor': BORDER,
                'gridColor': BORDER,
                'tickColor': BORDER,
                'labelColor': MUTED,
                'titleColor': TEXT,
                'labelFont': FONT,
                'titleFont': FONT,
            },
            'legend': {
                'labelColor': TEXT,
                'titleColor': TEXT,
                'labelFont': FONT,
                'titleFont': FONT,
            },
            'header': {
                'labelColor': TEXT,
                'titleColor': TEXT,
                'labelFont': FONT,
                'titleFont': FONT,
            },
            'concat': {'spacing': 12},
            'facet': {'spacing': 8},
        }
    }

alt.themes.register('dark_github', dark_theme)
alt.themes.enable('dark_github')

# %% [markdown]
# ## Interactive controls
# 
# - **City dropdown** — same as before, filters the whole dashboard by
#   `location`, compiled directly into the Vega-Lite spec (works after export,
#   no running kernel needed).
# - **Legend click-to-isolate** — bound to the weather-type legend; clicking a
#   category highlights it and fades the rest, an interaction that doesn't
#   depend on being able to tell colors apart.

# %% [code cell 5]
city_dropdown = alt.binding_select(
    options=['Seattle', 'New York'],
    name='City: '
)

city_select = alt.selection_point(
    name='city_select',
    fields=['location'],
    bind=city_dropdown,
    value='Seattle'
)

weather_legend_select = alt.selection_point(
    name='weather_legend_select',
    fields=['weather'],
    bind='legend'
)

# pan/zoom for the SPLOM
splom_zoom = alt.selection_interval(
    name='splom_zoom',
    bind='scales'
)

# %% [markdown]
# ## Build the three views

# %% [code cell 6]
splom = alt.Chart().mark_point(
    filled=True, size=18, opacity=0.55, color=SPLOM_COLOR
).encode(
    alt.X(alt.repeat('column'), type='quantitative'),
    alt.Y(alt.repeat('row'), type='quantitative'),
    tooltip=[
        alt.Tooltip(alt.repeat('column'), type='quantitative'),
        alt.Tooltip(alt.repeat('row'), type='quantitative'),
        alt.Tooltip('weather:N', title='Weather'),
        alt.Tooltip('date:T', title='Date'),
    ]
).add_params(
    splom_zoom
).properties(
    width=125,
    height=125
).repeat(
    row=['temp_max', 'precipitation', 'wind'],
    column=['wind', 'precipitation', 'temp_max']
)

# %% [code cell 7]
dateHist = alt.layer(
    alt.Chart().mark_bar().encode(
        alt.X('month(date):O', title='Month'),
        alt.Y(alt.repeat('row'), aggregate='average', type='quantitative'),
        tooltip=[
            alt.Tooltip('month(date):O', title='Month'),
            alt.Tooltip(alt.repeat('row'), aggregate='average', type='quantitative', format='.1f'),
        ]
    ),
    alt.Chart().mark_rule(stroke=WONG['vermillion'], strokeDash=[4, 3]).encode(
        alt.Y(alt.repeat('row'), aggregate='average', type='quantitative')
    )
).properties(
    width=175,
    height=125
).repeat(
    row=['temp_max', 'precipitation', 'wind']
)

# %% [code cell 8]
tempHist = alt.Chart().mark_bar().encode(
    alt.X('temp_max:Q', bin=True, title='Temperature (°C)'),
    alt.Y('count():Q'),
    alt.Color(
        'weather:N',
        scale=weather_colors,
        legend=alt.Legend(title='Weather (click to isolate)')
    ),
    opacity=alt.condition(weather_legend_select, alt.value(1.0), alt.value(0.15)),
    tooltip=[
        alt.Tooltip('weather:N', title='Weather'),
        alt.Tooltip('temp_max:Q', bin=True, title='Temp range (°C)'),
        alt.Tooltip('count():Q', title='Days'),
    ]
).transform_filter(
    city_select
).add_params(
    weather_legend_select
).properties(
    width=115,
    height=100
).facet(
    data=weather,
    column='weather:N'
)

# %% [markdown]
# ## Compose the dashboard
# 
# Same `vconcat(hconcat(splom, dateHist), tempHist)` layout as before, with the
# city dropdown registered at the top level.

# %% [code cell 9]
dashboard = alt.vconcat(
    alt.hconcat(splom, dateHist),
    tempHist,
    data=weather,
    title='Weather Dashboard'
).add_params(
    city_select
).transform_filter(
    city_select
).resolve_legend(
    color='independent'
).resolve_scale(
    color='independent'
).configure_axis(
    labelAngle=0
)

dashboard

# %% [markdown]
# ## Accessibility check
# 
# | Element | Color | Wong name |
# |---|---|---|
# | SPLOM points | `#D55E00` | vermillion |
# | drizzle | `#56B4E9` | sky blue |
# | fog | `#999999` | grey |
# | rain | `#0072B2` | blue |
# | snow | `#CC79A7` | reddish purple |
# | sun | `#E69F00` | orange |
# | mean rule (dashed) | `#D55E00` | vermillion |
# 
# Checked in [Coblis](https://www.color-blindness.com/coblis-color-blindness-simulator/)
# under protanopia, deuteranopia, and tritanopia — the SPLOM's vermillion stays
# clearly separable from the facet's blue `rain` category in every simulation.
# 
# On top of color, the dashboard now offers two color-independent ways to read
# the data: **tooltips** (exact numbers on hover) and the **click-to-isolate
# legend** (isolate one category by its text label, not just its color).

# %% [markdown]
# ## Export as a single, dark-themed HTML file

# %% [code cell 10]
html_str = dashboard.to_html()

# The chart's own dark background is baked into the Vega-Lite spec already;
# this adds a matching dark background to the surrounding HTML page itself.
page_style = f'''<style>
  html, body {{
    background: {BG};
    margin: 0;
    padding: 24px;
    font-family: {FONT};
  }}
</style>'''

html_str = html_str.replace('<head>', '<head>' + page_style, 1)

with open('homework5_weather_dashboard.html', 'w', encoding='utf-8') as f:
    f.write(html_str)

print('Saved homework5_weather_dashboard.html')
