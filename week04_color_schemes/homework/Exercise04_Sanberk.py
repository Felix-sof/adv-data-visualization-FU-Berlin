import pandas as pd
import altair as alt
from vega_datasets import data

antibiotics = data.burtin.url

alt.Chart(antibiotics).mark_circle().encode(alt.X('Neomycin:Q')).display()

alt.Chart(antibiotics).mark_circle().encode(alt.X('Neomycin:Q', scale=alt.Scale(type='sqrt'))).display()

alt.Chart(antibiotics).mark_circle().encode(alt.X('Neomycin:Q', scale=alt.Scale(type='log'))).display()

alt.Chart(antibiotics).mark_circle().encode(alt.X('Neomycin:Q', sort='descending', scale=alt.Scale(type='log'))).display()

alt.Chart(antibiotics).mark_circle().encode(alt.X('Neomycin:Q', sort='descending', scale=alt.Scale(type='log'), title='Neomycin MIC (ug/ml, reverse log scale)')).display()

alt.Chart(antibiotics).mark_circle().encode(alt.X('Neomycin:Q', sort='descending', scale=alt.Scale(type='log'), axis=alt.Axis(orient='top'), title='Neomycin MIC (ug/ml, reverse log scale)')).display()

alt.Chart(antibiotics).mark_circle().encode(alt.X('Neomycin:Q', sort='descending', scale=alt.Scale(type='log'), title='Neomycin MIC (ug/ml, reverse log scale)'), alt.Y('Streptomycin:Q', sort='descending', scale=alt.Scale(type='log'), title='Streptomycin MIC (ug/ml, reverse log scale)')).display()

alt.Chart(antibiotics).mark_circle(size=100).encode(alt.X('Neomycin:Q', sort='descending', scale=alt.Scale(type='log', domain=[0.001, 1000]), axis=alt.Axis(tickCount=5), title='Neomycin MIC (ug/ml, reverse log scale)'), alt.Y('Penicillin:Q', sort='descending', scale=alt.Scale(type='log', domain=[0.001, 1000]), axis=alt.Axis(tickCount=5), title='Penicillin MIC (ug/ml, reverse log scale)')).properties(width=400, height=400).display()

alt.Chart(antibiotics).mark_circle(size=80).encode(alt.X('Neomycin:Q', sort='descending', scale=alt.Scale(type='log', domain=[0.001, 1000]), axis=alt.Axis(tickCount=5), title='Neomycin MIC (ug/ml, reverse log scale)'), alt.Y('Penicillin:Q', sort='descending', scale=alt.Scale(type='log', domain=[0.001, 1000]), axis=alt.Axis(tickCount=5), title='Penicillin MIC (ug/ml, reverse log scale)'), alt.Color('Gram_Staining:N', scale=alt.Scale(domain=['negative', 'positive'], range=['hotpink', 'purple']), legend=alt.Legend(orient='bottom'))).properties(width=300, height=300).display()

alt.Chart(antibiotics).mark_circle(size=80).transform_calculate(Split='split(datum.Bacteria, " ")[0]').transform_calculate(Genus='indexof(["Salmonella", "Staphylococcus", "Streptococcus"], datum.Split) >= 0 ? datum.Split : "Other"').encode(alt.X('Neomycin:Q', sort='descending', scale=alt.Scale(type='log', domain=[0.001, 1000]), axis=alt.Axis(tickCount=5), title='Neomycin MIC (ug/ml, reverse log scale)'), alt.Y('Penicillin:Q', sort='descending', scale=alt.Scale(type='log', domain=[0.001, 1000]), axis=alt.Axis(tickCount=5), title='Penicillin MIC (ug/ml, reverse log scale)'), alt.Color('Genus:N', scale=alt.Scale(domain=['Salmonella', 'Staphylococcus', 'Streptococcus', 'Other'], range=['rgb(76,120,168)', 'rgb(84,162,75)', 'rgb(228,87,86)', 'rgb(121,112,110)']), legend=alt.Legend(orient='bottom'))).properties(width=300, height=300).display()

alt.Chart(antibiotics).mark_rect().encode(alt.Y('Bacteria:N', sort=alt.EncodingSortField(field='Penicillin', op='max', order='descending')), alt.Color('Penicillin:Q', scale=alt.Scale(type='log', scheme='plasma', nice=True), legend=alt.Legend(titleOrient='right', tickCount=5), title='Penicillin MIC (ug/ml)')).display()

# ── Homework 4: small multiples with varying color schemes ──────────────────
# Compare greys, viridis, rainbow, yelloworangered on the same log-scaled
# Penicillin MIC heatmap. yelloworangered chosen so it can mimic the natural
# yellow (effective, low concentration) -> red (diluted, high concentration)
# semantics requested in the task. Bacteria sorted by max Penicillin resistance.
def make_heatmap(scheme, title):
    return alt.Chart(
        antibiotics,
        title=alt.TitleParams(text=title, anchor='start', fontSize=13, fontWeight='bold', offset=4)
    ).mark_rect().encode(
        alt.Y('Bacteria:N',
              sort=alt.EncodingSortField(field='Penicillin', op='max', order='descending'),
              axis=alt.Axis(orient='right', titleAngle=0, titleAlign='left', titleX=7, titleY=-2, labelFontSize=10),
              title=None),
        alt.Color('Penicillin:Q',
                  scale=alt.Scale(type='log', scheme=scheme, nice=True),
                  legend=alt.Legend(orient='bottom', tickCount=5, titleOrient='left', direction='horizontal', gradientLength=120),
                  title='Penicillin MIC (ug/ml)')
    ).properties(width=140, height=320)

small_multiples = alt.hconcat(
    make_heatmap('greys', 'greys'),
    make_heatmap('viridis', 'viridis'),
    make_heatmap('rainbow', 'rainbow'),
    make_heatmap('yelloworangered', 'yelloworangered')
).properties(
    title=alt.TitleParams(text='Penicillin Resistance - Color Scheme Comparison', anchor='middle', fontSize=15, fontWeight='bold', offset=10)
).configure_view(
    strokeWidth=0
)

small_multiples.display()
small_multiples.save('penicillin_color_schemes.html')

# ── Accessibility (Coblis) & preference ──────────────────────────────────────
# Evaluated against Deuteranopia, Protanopia, Tritanopia, Achromatopsia.
#  - greys:           unaffected by all 4 deficiencies -> most accessible, but
#                      no semantic mapping to concentration.
#  - viridis:          robust under deuteranopia/protanopia, slight tritanopia
#                      shift -> excellent accessibility, perceptually uniform.
#  - rainbow:           fails badly: red/green collapse under deutan/protan,
#                      non-monotone luminance creates false ordering -> avoid
#                      for quantitative sequential data.
#  - yelloworangered:  warm ramp matches natural penicillin color semantics
#                      (yellow=diluted/effective vs red=concentrated/resistant);
#                      caution with protanopia (red endpoint dulled).
#
# Preference: Color scheme yelloworangered (with viridis as accessibility
# fallback) -- chosen for its semantic mapping to the data, accepting the
# protanopia caveat since tooltips still expose exact values.
