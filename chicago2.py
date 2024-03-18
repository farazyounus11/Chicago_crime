import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk

df = pd.read_csv("chicagodata.csv")

df['Date'] = pd.to_datetime(df['Date'])

min_date = df['Date'].min().to_pydatetime()
max_date = df['Date'].max().to_pydatetime()

default_start_date = min_date
default_end_date = max_date

selected_start_date, selected_end_date = st.sidebar.slider(
    "Select date range",
    min_value=min_date,
    max_value=max_date,
    value=(default_start_date, default_end_date)
)

crime_types = df['Primary Type'].unique()
selected_crime_types = st.sidebar.multiselect(
    "Select crime types",
    crime_types,
    default=None
)

descriptions = df[df['Primary Type'].isin(selected_crime_types)]['Description'].unique()
selected_descriptions = st.sidebar.multiselect(
    "Select descriptions",
    descriptions,
    default=descriptions
)

st.sidebar.write("Selected start date:", selected_start_date)
st.sidebar.write("Selected end date:", selected_end_date)

filtered_df = df[
    (df['Date'] >= pd.to_datetime(selected_start_date)) & 
    (df['Date'] <= pd.to_datetime(selected_end_date)) &
    (df['Primary Type'].isin(selected_crime_types)) &
    (df['Description'].isin(selected_descriptions))
]

st.title("Chicago Crime Visualization")
st.header('By Faraz Younus | M.S. Statistics & Data Science', divider='gray')

st.write(filtered_df)

st.header('Stats')

number_of_crimes = len(filtered_df)
true_arrest_count = filtered_df['Arrest'].sum()
col1, col2 = st.columns(2)

with col1:
    st.metric(label="Number of Crimes", value=number_of_crimes)
with col2:
    st.metric(label="Arrest Rate", value=(true_arrest_count/number_of_crimes)*100)
    

st.header('Scatter Chart', divider='gray')

grouped = df.groupby(['Date', 'PrimaryType']).size().reset_index(name='Counts')

# Now, prepare for visualization in Streamlit (conceptual; adapt as needed)
# Option 1: Plot each PrimaryType in its own chart
for primary_type in grouped['PrimaryType'].unique():
    subset = grouped[grouped['PrimaryType'] == primary_type]
    st.write(f"Primary Type: {primary_type}")
    st.scatter_chart(subset[['Date', 'Counts']])

st.header('Map', divider='gray')

st.pydeck_chart(pdk.Deck(
    map_style=None,
    initial_view_state=pdk.ViewState(
        latitude=41.76,
        longitude=-87.6,
        zoom=11,
        pitch=50,
    ),
    layers=[
        pdk.Layer(
            'HexagonLayer',
            data=filtered_df,
            get_position='[lon, lat]',
            radius=100,
            elevation_scale=3,
            elevation_range=[0, 1000],
            pickable=True,
            extruded=True,
        ),
        pdk.Layer(
            'ScatterplotLayer',
            data=filtered_df,
            get_position='[lon, lat]',
            get_color='[200, 30, 0, 160]',
            get_radius=100,
        ),
    ],
))
