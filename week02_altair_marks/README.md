# Week 02 — Interactive Filtering & Concatenation

## 📋 Homework Task

Adapt the "A Peek Ahead: Interactive Filtering" plot to visualize not only 
population change over time, but also life expectancy and fertility. 
The three plots should be concatenated horizontally and linked to a shared slider.
Submitted as a standalone HTML visualization.

## 🛠️ What I Implemented
- Loaded gapminder dataset with population, life expectancy and fertility data
- Built a shared slider parameter (1955–2005, step 5) linked across all three charts
- Implemented mouseover highlight selection to trace individual countries
- Scatter plot: fertility vs life expectancy, bubble size = population
- Line chart: life expectancy trends over time per country
- Line chart: fertility trends over time per country
- Linked all three charts horizontally with `alt.hconcat()`
- Exported as standalone HTML dashboard

## 🔧 Technologies
`Python 3.11` · `Altair 5` · `Pandas` · `vega_datasets` · `JupyterLab`