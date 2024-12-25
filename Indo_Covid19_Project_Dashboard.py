import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt

# Load dataset
# The 'Date' column is converted to a datetime format for filtering and analysis.
df = pd.read_csv("covid_19_indonesia_time_series_all.csv")
df['Date'] = pd.to_datetime(df['Date'])

# --- TITLE & INTRO ---
st.title("COVID-19 Indonesia Dashboard :bar_chart:")
st.markdown("""
Explore COVID-19 trends, key metrics, and insights across Indonesia using this interactive dashboard. 
Filter data by date and province to dynamically view trends and statistics.
""")


# Sidebar Filters
# Add filters in the sidebar to allow users to customize the data being displayed.
st.sidebar.header("Filters") # Sidebar header

# Date range filter for selecting a start and end date.
date_range = st.sidebar.date_input("Select Date Range", 
                                  [df['Date'].min(), df['Date'].max()]) # Default range: full dataset range

# Dropdown filter for selecting a specific province or viewing all province.
province = st.sidebar.selectbox("Select Province", 
                                options=['All'] + list(df['Province'].unique()))

# Apply Filters
# Filter the dataset based on the selected date range.
filtered_df = df[(df['Date'] >= pd.to_datetime(date_range[0])) & 
                 (df['Date'] <= pd.to_datetime(date_range[1]))]

# If a specific province is selected, further filter the dataset.
if province != 'All':
    filtered_df = filtered_df[filtered_df['Province'] == province]

# KPIs
# Display summary statistics to provide a quick overview of key COVID-19 metrics.
st.subheader("Key Metrics")

# Display the total cases, deaths, and recovered cases in a formatted mannner.
st.write(f"Total Cases: {filtered_df['Total Cases'].max():,}")
st.write(f"Total Deaths: {filtered_df['Total Deaths'].max():,}")
st.write(f"Total Recovered: {filtered_df['Total Recovered'].max():,}")


# Visualizations

# Line chart for daily new cases trend
st.subheader("Daily New Cases Trend")
fig = px.line(filtered_df, x="Date", y="New Cases", title="Daily New Cases") # Title for the chart
st.plotly_chart(fig) # Render the Plotly chart in Streamlit


# Bar chart for the top 10 provinces by total cases
st.subheader("Top 10 Provinces by Total Cases")
top_provinces = filtered_df.groupby("Province")["Total Cases"].max().nlargest(10)
st.bar_chart(top_provinces) # Render the bar chart

# Choropleth map to visualize COVID-19 spread geographically
st.subheader("COVID-19 Spread by Location")
fig_map = px.choropleth(filtered_df, 
                        locations="Location ISO Code", # Geographic identifiers 
                        color="Total Cases", # Color intensity based on total cases 
                        hover_name="Province", # Display province names on hover
                        title="Geographical Spread of Cases")
st.plotly_chart(fig_map) # Render the map in Streamlit


# Pie Chart for Distribution of Total Cases
st.subheader("Distribution of Total Cases: Recovered vs. Active vs. Deaths")

# Calculate the proportion of each category (Active, Recovered, Deaths)
total_cases = filtered_df['Total Cases'].max()
recovered = filtered_df['Total Recovered'].max()
deaths = filtered_df['Total Deaths'].max()
active_cases = total_cases - (recovered + deaths)

# Data for Pie chart
# Define Labels and sizes for the pie chart.
labels = ['Recovered', 'Deaths', 'Active Cases']
sizes = [recovered, deaths, active_cases]
explode = (0.1, 0, 0)  # Slightly "explode" the recoverd slice for emphasis.

# Create a pie chart using Matplotlib
fig, ax = plt.subplots()
ax.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%', shadow=True, startangle=140) # Startangle: Adjust starting angle for better layout
ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

st.pyplot(fig)  # Render the pie chart in Streamlit

# Show Raw Data
st.subheader("Raw Data")
st.dataframe(filtered_df) # Display the filterd data in a table format.


# --- FOOTER ---
st.markdown("""
*Developed with [Streamlit](https://streamlit.io/)* | 
**Data Source:** [Kaggle COVID-19 Indonesia Dataset](https://www.kaggle.com/datasets/hendratno/covid19-indonesia)
""")