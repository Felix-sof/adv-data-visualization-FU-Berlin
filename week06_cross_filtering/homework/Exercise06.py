import altair as alt

movies = 'https://cdn.jsdelivr.net/npm/vega-datasets@1/data/movies.json'
fields = ['IMDB_Rating', 'Rotten_Tomatoes_Rating', 'IMDB_Votes', 'Worldwide_Gross']

# shared selections: rating radio filter, global brush, legend highlight
mpaa_filter = alt.selection_point(
    name='mpaa_filter',
    fields=['MPAA_Rating'],
    bind=alt.binding_radio(options=['G', 'PG', 'PG-13', 'R', 'NC-17', 'Not Rated'], name='MPAA Rating: ')
)
splom_brush = alt.selection_interval(name='splom_brush', resolve='global')
genre_highlight = alt.selection_point(name='genre_highlight', fields=['Major_Genre'], bind='legend')

# SPLOM, colored by genre, greyed out unless inside the brush
splom = alt.Chart(movies).mark_circle(size=35).encode(
    x=alt.X(alt.repeat('column'), type='quantitative'),
    y=alt.Y(alt.repeat('row'), type='quantitative'),
    color=alt.condition(
        splom_brush,
        alt.Color('Major_Genre:N', legend=alt.Legend(title='Genre  (click to highlight)', orient='right')),
        alt.value('lightgrey')
    ),
    opacity=alt.condition(mpaa_filter & genre_highlight, alt.value(0.85), alt.value(0.04)),
    tooltip=['Title:N', 'Major_Genre:N', 'MPAA_Rating:N', 'IMDB_Rating:Q', 'Rotten_Tomatoes_Rating:Q']
).properties(
    width=155, height=155
).add_params(
    splom_brush, mpaa_filter, genre_highlight
).repeat(
    row=fields, column=fields
)

# genre bar chart: grey = MPAA-filtered total, colored = all three filters applied
bg = alt.Chart().mark_bar(color='#e0e0e0').encode(
    x=alt.X('count():Q', title='Number of Films'),
    y=alt.Y('Major_Genre:N', sort='-x', title=None)
).transform_filter(mpaa_filter)

fg = alt.Chart().mark_bar().encode(
    x='count():Q',
    y=alt.Y('Major_Genre:N', sort='-x', title=None),
    color=alt.Color('Major_Genre:N', legend=None),
    tooltip=['Major_Genre:N', 'count():Q']
).transform_filter(splom_brush).transform_filter(mpaa_filter).transform_filter(genre_highlight)

genre_bar = alt.layer(bg, fg, data=movies).properties(
    width=640, height=220,
    title=alt.Title('Films per Genre — updates with brush & MPAA filter', anchor='start', color='#666', fontSize=12)
)

# live count of films matching all three filters
label = alt.Chart().mark_text(align='right', color='#555', fontSize=13, fontStyle='italic').encode(
    text=alt.value('films in selection →'), x=alt.value(490), y=alt.value(16)
)

count_text = alt.Chart(movies).mark_text(align='left', color='#e45756', fontSize=15, fontWeight='bold').encode(
    text=alt.Text('count:Q', format='.0f'), x=alt.value(500), y=alt.value(16)
).transform_filter(splom_brush).transform_filter(mpaa_filter).transform_filter(genre_highlight).transform_aggregate(count='count()')

count_label = alt.layer(label, count_text).properties(width=660, height=30)

# compose + export
dashboard = alt.vconcat(
    count_label, splom, genre_bar,
    spacing=6,
    title=alt.Title('Movie Ratings Explorer — SPLOM by Genre & MPAA Rating', anchor='middle', dy=-4, fontSize=20)
).configure_view(
    continuousWidth=300, continuousHeight=300, stroke='transparent'
).configure_axis(
    labelFontSize=10, titleFontSize=11
).configure_legend(
    labelFontSize=10, titleFontSize=11
)

html_str = dashboard.to_html()
# center the MPAA radio buttons underneath the chart
style = '<style>form.vega-bindings{display:flex;justify-content:center;gap:12px;margin-top:8px;}</style>'
html_str = html_str.replace('<head>', '<head>' + style, 1)

with open('homework6_movie_ratings_explorer.html', 'w', encoding='utf-8') as f:
    f.write(html_str)

dashboard
