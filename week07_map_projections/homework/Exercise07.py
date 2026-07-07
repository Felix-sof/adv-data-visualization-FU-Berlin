import altair as alt
from vega_datasets import data

counties = alt.topo_feature(data.us_10m.url, "counties")
unemp = data.unemployment.url

# exclude Alaska (02), Hawaii (15), Puerto Rico (72) so every projection
# frames only the 48 contiguous states
EXCLUDED_FIPS = ["02", "15", "72"]
exclude_expr = " && ".join([f"datum.state_fips != '{f}'" for f in EXCLUDED_FIPS])


def make_map(projection_type):
    hover = alt.selection_point(on="mouseover", fields=["id"], empty=False, name=f"hover_{projection_type}")

    return (
        alt.Chart(counties)
        .transform_calculate(state_fips="substring(format(datum.id, '05d'), 0, 2)")
        .transform_filter(exclude_expr)
        .mark_geoshape(stroke="white", strokeWidth=0.1)
        .transform_lookup(lookup="id", from_=alt.LookupData(data=unemp, key="id", fields=["rate"]))
        .encode(
            color=alt.Color("rate:Q", title="Unemployment Rate", scale=alt.Scale(scheme="viridis", domain=[0, 0.25])),
            tooltip=[alt.Tooltip("rate:Q", title="Rate", format=".1%")],
            opacity=alt.condition(hover, alt.value(1), alt.value(0.85)),
            stroke=alt.condition(hover, alt.value("black"), alt.value("white")),
            strokeWidth=alt.condition(hover, alt.value(1.2), alt.value(0.1)),
        )
        .add_params(hover)
        .project(type=projection_type)
        .properties(width=350, height=250, title=projection_type)
        .interactive(name=f"zoom_{projection_type}")
    )


# small multiple: compare unemployment rate across four US projections
chart = alt.vconcat(
    alt.hconcat(make_map("albersUsa"), make_map("albers")),
    alt.hconcat(make_map("conicEqualArea"), make_map("conicConformal")),
).properties(
    title=alt.TitleParams(
        text="US County Unemployment Rates Across Different Map Projections (Contiguous US)",
        subtitle=[
            "Favorite projection: Albers USA — designed specifically for the United States.",
            "It preserves area and repositions Alaska & Hawaii for a compact national view.",
        ],
        subtitleFontSize=12,
        subtitleColor="#666",
        anchor="middle",
    )
)

chart.save("Homework7_Unemployment_Projections_Interactive.html")
chart
