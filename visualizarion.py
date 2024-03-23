import streamlit as st
import folium
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
from streamlit_folium import folium_static
from geopy.geocoders import Nominatim


def show_visualization():
    st.subheader("Visualization Page")

    st.write("### Line Plot")
    show_line_plot()

    st.write("### Scatter Plot")
    show_scatter_plot()

    st.write("### Histogram")
    show_histogram()

    st.write("### Heatmap")
    show_heatmap()

def show_line_plot():
    # Generate sample data
    x = np.linspace(0, 10, 100)
    y = np.sin(x)
    fig, ax = plt.subplots()
    ax.plot(x, y)
    st.pyplot(fig)

def show_scatter_plot():
    # Generate sample data
    x = np.random.randn(100)
    y = np.random.randn(100)
    fig, ax = plt.subplots()
    ax.scatter(x, y)
    st.pyplot(fig)

def show_histogram():
    # Generate sample data
    data = np.random.randn(1000)
    fig, ax = plt.subplots()
    ax.hist(data, bins=30)
    st.pyplot(fig)

def show_heatmap():
    # Generate sample data
    data = np.random.rand(100, 3)
    m = folium.Map([0, 0], zoom_start=2)
    heat_data = [[row['lat'],row['lon']] for index, row in pd.DataFrame(data, columns=['lat', 'lon', 'weight']).iterrows()]
    m.add_child(folium.plugins.HeatMap(heat_data))
    folium_static(m)
show_visualization()
