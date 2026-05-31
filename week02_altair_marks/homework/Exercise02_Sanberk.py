#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd
import altair as alt
from vega_datasets import data

df = data.gapminder()

# SLIDER
year_slider = alt.binding_range(min=1955, max=2005, step=5)
year_select = alt.param(
    name='year_select',
    bind=year_slider,
    value=2000
)

# HOVER
highlight = alt.selection_point(
    name='highlight',
    on='mouseover',
    fields=['country'],
    empty='none'
)

# -------------------
# BASE (TEK YERDE PARAM)
# -------------------
base = alt.Chart(df).add_params(
    year_select,
    highlight
)

# -------------------
# 1️⃣ SCATTER
# -------------------
scatter = base.transform_filter(
    alt.datum.year == year_select
).mark_circle(opacity=0.7).encode(
    x=alt.X('fertility:Q'),
    y=alt.Y('life_expect:Q'),
    size=alt.Size('pop:Q', scale=alt.Scale(range=[20,1000])),
    color=alt.Color('cluster:N', legend=None),
    tooltip=['country:N','fertility:Q','life_expect:Q','pop:Q']
)

# -------------------
# 2️⃣ LIFE
# -------------------
life_trend = base.mark_line().encode(
    x='year:O',
    y='life_expect:Q',
    detail='country:N',

    color=alt.condition(
        highlight,
        alt.Color('country:N', legend=None),
        alt.value('lightgray')
    ),

    size=alt.condition(highlight, alt.value(3), alt.value(1)),
    opacity=alt.condition(highlight, alt.value(1), alt.value(0.1)),

    tooltip=['country:N','year:O','life_expect:Q']
)

# -------------------
# 3️⃣ FERTILITY
# -------------------
fertility_trend = base.mark_line().encode(
    x='year:O',
    y='fertility:Q',
    detail='country:N',

    color=alt.condition(
        highlight,
        alt.Color('country:N', legend=None),
        alt.value('lightgray')
    ),

    size=alt.condition(highlight, alt.value(3), alt.value(1)),
    opacity=alt.condition(highlight, alt.value(1), alt.value(0.1)),

    tooltip=['country:N','year:O','fertility:Q']
)

# CONCAT
final_chart = alt.hconcat(
    scatter,
    life_trend,
    fertility_trend
).properties(
    title='Global Development Dashboard'
)

