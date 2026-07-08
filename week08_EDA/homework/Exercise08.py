import numpy as np
import pandas as pd
import requests
import altair as alt
from sklearn.feature_selection import mutual_info_regression


import datetime

mortality_url = "https://raw.githubusercontent.com/akarlinsky/world_mortality/main/world_mortality.csv"
mortality_raw = pd.read_csv(mortality_url)

deaths_de = mortality_raw[
    (mortality_raw['country_name'] == 'Germany') &
    (mortality_raw['time_unit'] == 'weekly')
].copy()

def iso_week_to_date(row):
    return datetime.datetime.strptime(f"{int(row['year'])}-W{int(row['time']):02d}-1", "%G-W%V-%w")

deaths_de['week_start'] = deaths_de.apply(iso_week_to_date, axis=1)
deaths_de = deaths_de[['week_start', 'year', 'deaths']].reset_index(drop=True)

deaths_de.tail(10)

berlin_lat, berlin_lon = 52.52, 13.405

response = requests.get(
    "https://archive-api.open-meteo.com/v1/archive",
    params={
        "latitude": berlin_lat,
        "longitude": berlin_lon,
        "start_date": "2015-01-01",
        "end_date": "2024-12-31",
        "daily": "temperature_2m_max,temperature_2m_min,temperature_2m_mean",
        "timezone": "Europe/Berlin",
    },
    timeout=30,
)
response.raise_for_status()
weather_json = response.json()

temp_daily = pd.DataFrame({
    "date": pd.to_datetime(weather_json["daily"]["time"]),
    "temp_max": weather_json["daily"]["temperature_2m_max"],
    "temp_min": weather_json["daily"]["temperature_2m_min"],
    "temp_mean": weather_json["daily"]["temperature_2m_mean"],
})

temp_daily.head()

temp_daily['week_start'] = temp_daily['date'].dt.to_period('W-SUN').apply(lambda p: p.start_time)

temp_weekly = temp_daily.groupby('week_start').agg(
    temp_mean=('temp_mean', 'mean'),
    temp_max=('temp_max', 'max'),
    temp_min=('temp_min', 'min'),
).reset_index()

temp_weekly.head()

data_heat = pd.merge(deaths_de, temp_weekly, on='week_start', how='inner')

data_heat['season'] = data_heat['week_start'].dt.month.map({
    12: 'Winter', 1: 'Winter', 2: 'Winter',
    3: 'Spring', 4: 'Spring', 5: 'Spring',
    6: 'Summer', 7: 'Summer', 8: 'Summer',
    9: 'Autumn', 10: 'Autumn', 11: 'Autumn',
})
data_heat['heatwave_week'] = data_heat['temp_max'] > 30   # simple >30°C threshold

data_heat.tail(10)

data_heat.info()

data_heat[['deaths', 'temp_mean', 'temp_max', 'temp_min']].describe()

def create_corr_chart(data, cols):

    corr = data[cols].corr(method='pearson').reset_index().melt('index')
    corr.columns = ['var_1', 'var_2', 'correlation']

    chart = alt.Chart(corr).mark_rect().encode(
        alt.X('var_1', title=None, axis=alt.Axis(labelAngle=-45)),
        alt.Y('var_2', title=None),
        alt.Color('correlation', legend=None, scale=alt.Scale(scheme='redblue', reverse=True)),
    ).properties(
        width=alt.Step(60),
        height=alt.Step(60)
    )

    chart += chart.mark_text(size=13).encode(
        alt.Text('correlation', format=".2f"),
        color=alt.condition("abs(datum.correlation) > 0.5", alt.value('white'), alt.value('black'))
    )

    return chart

numeric_cols = ['deaths', 'temp_mean', 'temp_max', 'temp_min']
chart_corr_heat = create_corr_chart(data_heat, numeric_cols)
chart_corr_heat

def create_corr_chart_upper(data, cols):
    corr = data[cols].corr(method='pearson').reset_index().melt('index')
    corr.columns = ['var_1', 'var_2', 'correlation']

    chart = alt.Chart(corr).mark_rect().encode(
        alt.X('var_1', title=None, axis=alt.Axis(labelAngle=-45)),
        alt.Y('var_2', title=None),
        alt.Color('correlation', legend=None, scale=alt.Scale(scheme='redblue', reverse=True)),
    ).properties(width=alt.Step(60), height=alt.Step(60))

    chart += chart.mark_text(size=13).encode(
        alt.Text('correlation', format=".2f"),
        color=alt.condition("abs(datum.correlation) > 0.5", alt.value('white'), alt.value('black'))
    )

    return chart.transform_filter("datum.var_1 > datum.var_2")

create_corr_chart_upper(data_heat, numeric_cols)

def create_mi_chart(data, cols):
    n = len(cols)
    mi_matrix = np.zeros((n, n))

    for i, target_col in enumerate(cols):
        mi_matrix[:, i] = mutual_info_regression(
            data[cols].values, data[target_col].values, random_state=0
        )

    mi_df = pd.DataFrame(mi_matrix, index=cols, columns=cols).reset_index().melt('index')
    mi_df.columns = ['var_1', 'var_2', 'mutual_info']

    chart = alt.Chart(mi_df).mark_rect().encode(
        alt.X('var_1', title=None, axis=alt.Axis(labelAngle=-45)),
        alt.Y('var_2', title=None),
        alt.Color('mutual_info', legend=None, scale=alt.Scale(scheme='greens')),
    ).properties(width=alt.Step(60), height=alt.Step(60))

    chart += chart.mark_text(size=12).encode(
        alt.Text('mutual_info', format=".2f"),
        color=alt.condition("datum.mutual_info > 1.5", alt.value('white'), alt.value('black'))
    )

    return chart

create_mi_chart(data_heat, numeric_cols)

def create_parallel_chart(data, cols, color_col):
    new_data = data.reset_index()[['index', color_col] + cols].melt(id_vars=['index', color_col])

    chart = alt.Chart(new_data).mark_line().encode(
        alt.X('variable:N'),
        alt.Y('value:Q'),
        alt.Color(f'{color_col}:N', scale=alt.Scale(scheme='category10')),
        alt.Detail('index:N'),
        opacity=alt.value(0.35),
    ).properties(width=700)

    return chart

chart_parallel_heat = create_parallel_chart(data_heat, numeric_cols, 'season')
chart_parallel_heat

from sklearn.preprocessing import StandardScaler

scaler_heat = StandardScaler()
scaled_values = scaler_heat.fit_transform(data_heat[numeric_cols])
scaled_data_heat = pd.DataFrame(scaled_values, columns=numeric_cols)
scaled_data_heat['season'] = data_heat['season'].values

scaled_data_heat.head()

chart_parallel_scaled_heat = create_parallel_chart(scaled_data_heat, numeric_cols, 'season')
chart_parallel_scaled_heat

reordered_cols = ['temp_min', 'temp_mean', 'deaths', 'temp_max']
create_parallel_chart(scaled_data_heat[reordered_cols + ['season']], reordered_cols, 'season')

from sklearn.preprocessing import MinMaxScaler

normalizer_heat = MinMaxScaler()
normalized_values = normalizer_heat.fit_transform(data_heat[numeric_cols])
normalized_data_heat = pd.DataFrame(normalized_values, columns=numeric_cols)
normalized_data_heat['season'] = data_heat['season'].values

create_parallel_chart(normalized_data_heat, numeric_cols, 'season')

hover_season = alt.selection_point(fields=['season'], on='mouseover', nearest=False, empty='none')

new_data = scaled_data_heat.reset_index()[['index', 'season'] + numeric_cols].melt(id_vars=['index', 'season'])

chart_hover = alt.Chart(new_data).mark_line().add_params(hover_season).encode(
    alt.X('variable:N'),
    alt.Y('value:Q'),
    alt.Color('season:N', scale=alt.Scale(scheme='category10')),
    alt.Detail('index:N'),
    opacity=alt.condition(hover_season, alt.value(0.85), alt.value(0.05)),
).properties(width=700, title='Hover near a line to highlight its season')

chart_hover

def create_scatter_matrix(data, cols, color_col):
    chart = alt.Chart(data).mark_circle(size=40).encode(
        alt.X(alt.repeat("column"), type='quantitative', scale=alt.Scale(nice=True)),
        alt.Y(alt.repeat("row"), type='quantitative', scale=alt.Scale(nice=True)),
        color=f'{color_col}:N'
    ).properties(
        width=150,
        height=150
    ).repeat(
        row=cols,
        column=cols
    )

    return chart

chart_scatter_heat = create_scatter_matrix(data_heat, numeric_cols, 'season')
chart_scatter_heat

brush = alt.selection_interval(resolve='global')

base_brushed = alt.Chart(data_heat).mark_circle(size=40).add_params(brush).encode(
    alt.X(alt.repeat("column"), type='quantitative', scale=alt.Scale(nice=True)),
    alt.Y(alt.repeat("row"), type='quantitative', scale=alt.Scale(nice=True)),
    color=alt.condition(brush, 'season:N', alt.value('lightgrey')),
    tooltip=[alt.Tooltip('week_start:T', title='Week'),
             alt.Tooltip('deaths:Q', title='Deaths'),
             alt.Tooltip('temp_mean:Q', title='Mean Temp (°C)', format='.1f')]
).properties(width=150, height=150)

chart_scatter_brushed = base_brushed.repeat(row=numeric_cols, column=numeric_cols)
chart_scatter_brushed


lower_triangle_rows = []
for i, row_var in enumerate(numeric_cols):
    row_charts = []
    for j, col_var in enumerate(numeric_cols):
        if j <= i:  # lower triangle + diagonal
            cell = alt.Chart(data_heat).mark_circle(size=35).add_params(brush).encode(
                x=alt.X(col_var, type='quantitative', scale=alt.Scale(nice=True)),
                y=alt.Y(row_var, type='quantitative', scale=alt.Scale(nice=True)),
                color=alt.condition(brush, 'season:N', alt.value('lightgrey')),
            ).properties(width=130, height=130)
            row_charts.append(cell)
    lower_triangle_rows.append(alt.hconcat(*row_charts))

chart_lower_triangle = alt.vconcat(*lower_triangle_rows)
chart_lower_triangle

final_dashboard = alt.vconcat(
    alt.hconcat(chart_corr_heat, create_mi_chart(data_heat, numeric_cols)),
    chart_parallel_scaled_heat,
    chart_scatter_brushed,
).resolve_scale(color='independent')

final_dashboard.save('homework8_heat_mortality.html')
print("Saved homework8_heat_mortality.html")
