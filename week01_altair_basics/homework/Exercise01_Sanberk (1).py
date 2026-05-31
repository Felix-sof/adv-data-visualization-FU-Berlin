import pandas as pd
import altair as alt
from vega_datasets import data


cars = data.cars()


cars = cars[cars['Origin'].isin(['USA', 'Europe', 'Japan'])]


brush = alt.selection_interval()


overview = alt.Chart(cars).mark_point().encode(
    x='Year:T',
    y='Miles_per_Gallon:Q',
    color='Origin:N',
    tooltip=['Name', 'Origin', 'Year', 'Miles_per_Gallon']
).properties(
    width=600,
    height=300,
    title="Overview"
).add_params(
    brush
)


detail = alt.Chart(cars).mark_point().encode(
    x='Horsepower:Q',
    y='Miles_per_Gallon:Q',
    color='Origin:N',
    tooltip=['Name', 'Origin', 'Horsepower']
).transform_filter(
    brush
).properties(
    width=600,
    height=300,
    title="Detail (Filtered)"
)


chart = overview & detail


chart.save('homework.html')

chart
