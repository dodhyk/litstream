import pandas as pd
import numpy as np
import streamlit as st

df = pd.read_csv('fpl.csv')

df['90s'] = df['minutes']/90
calc_elements = ['goals', 'assists', 'points']
for each in calc_elements:
    df[f'{each}_p90'] = df[each] / df['90s']

positions = list(df['position'].drop_duplicates())
teams = list(df['team'].drop_duplicates()) 

position_choice = st.sidebar.multiselect(
    'Choose position:', positions, default=positions
)

team_choice = st.sidebar.multiselect(
    'Choose Teams:', teams, default=teams
)

price_choice = st.sidebar.slider(
    'Max Price:', min_value=4.0, max_value=15.0, step=5.0, value=15.0
)

df = df[df['position'].isin(position_choice)]
df = df[df['team'].isin(team_choice)]
df = df[df['cost'] < price_choice]

# Visualization
st.title(f"Fantasy Football Analysis")
st.markdown('### Player Dataframe')
st.dataframe(df.sort_values('points', ascending=False).reset_index(drop=True))

st.markdown('### Cost vs 20/21 Points')
st.vega_lite_chart(df, {
    'mark': {'type': 'circle', 'tooltip': True},
    'encoding': {
        'x' : {'field': 'cost', 'type': 'quantitative'},
        'y': {'field': 'points', 'type':'quantitative'},
        'color': {'field':'position', 'type': 'nominal'},
        'tooltip': [{'field': 'name', 'type': 'nominal'}, {'field' : 'cost', 'type':'quantitative'}, {'field':'points', 'type':'quantitative'}],
    },
    'width': 700,
    'height': 400,
})