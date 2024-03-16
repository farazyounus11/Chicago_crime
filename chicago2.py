import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk

shareable_link = 'https://drive.google.com/file/d/1qmYH1ngyG2h0K4ec0vHM9MqPPyCZtV3R/view?usp=sharing'

df = pd.read_csv(shareable_link)

# Convert 'Date' column to datetime format
df['Date'] = pd.to_datetime(df['Date'])

# Find the minimum and maximum dates for the slider
min_date = df['Date'].min().to_pydatetime()
max_date = df['Date'].max().to_pydatetime()

# Set default values for the start and end dates
default_start_date = min_date
default_end_date = max_date

# Create a date range slider
selected_start_date, selected_end_date = st.sidebar.slider(
    "Select date range",
    min_value=min_date,
    max_value=max_date,
    value=(default_start_date, default_end_date)
)

# Select crime types
crime_types = df['Primary Type'].unique()
selected_crime_types = st.sidebar.multiselect(
    "Select crime types",
    crime_types,
    default=crime_types
)

# NEW: Select descriptions based on the filtered crime types
descriptions = df[df['Primary Type'].isin(selected_crime_types)]['Description'].unique()
selected_descriptions = st.sidebar.multiselect(
    "Select descriptions",
    descriptions,
    default=descriptions
)

# Display selected filters
st.sidebar.write("Selected start date:", selected_start_date)
st.sidebar.write("Selected end date:", selected_end_date)


# Filter DataFrame based on selected date range, crime types, and descriptions
filtered_df = df[
    (df['Date'] >= pd.to_datetime(selected_start_date)) & 
    (df['Date'] <= pd.to_datetime(selected_end_date)) &
    (df['Primary Type'].isin(selected_crime_types)) &
    (df['Description'].isin(selected_descriptions))
]

# Display the filtered DataFrame
st.write(filtered_df)


# Display the map visualization for the filtered DataFrame
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



number_of_crimes = len(filtered_df)
true_arrest_count = filtered_df['Arrest'].sum()
col1, col2 = st.columns(2)

with col1:
    st.metric(label="Number of Crimes", value=number_of_crimes)
with col2:
    st.metric(label="Arrest Rate", value=(true_arrest_count/number_of_crimes)*100)
