import streamlit as st
import folium
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
from streamlit_folium import folium_static
from geopy.geocoders import Nominatim
import pickle

# Load the pre-trained model
with open('model.pickle', 'rb') as f:
    model = pickle.load(f)

# Define function to take inputs and make predictions
def predict_temperature(depthm, T_degC, Salnty, O2ml_L, STheta, O2Sat, Oxy_µmol_Kg):
    # Prepare input data as a DataFrame
    input_data = pd.DataFrame({
        'Depthm': [depthm],
        'T_degC': [T_degC],
        'Salnty': [Salnty],
        'O2ml_L': [O2ml_L],
        'STheta': [STheta],
        'O2Sat': [O2Sat],
        'Oxy_µmol/Kg': [Oxy_µmol_Kg]
    })
    
    # Make prediction
    prediction = model.predict(input_data)
    return prediction

def main():
    st.title('Team Gamma')

    page = st.sidebar.selectbox("Select a page", ["Home", "Location Picker", "Visualization"])

    if page == "Home":
        home()
    elif page == "Location Picker":
        location_picker()
    elif page == "Visualization":
        visualization()

def home():
    st.title('Ocean Safety Prediction')

    # Input fields
    depthm = st.number_input('Depth (m)', min_value=0.0, step=1.0)
    T_degC = st.number_input('Temperature (°C)')
    Salnty = st.number_input('Salinity')
    O2ml_L = st.number_input('Oxygen (ml/L)')
    STheta = st.number_input('Sigma-theta')
    O2Sat = st.number_input('Oxygen Saturation (%)')
    Oxy_µmol_Kg = st.number_input('Oxygen (µmol/Kg)')
    phone_number = st.text_input('Enter your phone number')

    # Prediction button
    if st.button('Predict Fishing'):
        prediction = predict_temperature(depthm, T_degC, Salnty, O2ml_L, STheta, O2Sat, Oxy_µmol_Kg)
        st.write(
            'Fishing is Not Good!' if prediction[0] else 'Fishing is Perfect!')
        if(prediction[0]):
            st.button('alert')
        else:
            st.button('safe')

        
def location_picker():
    st.title("Location Picker")

    # Create a map centered around a default location
    map_center = [40.7128, -74.0060]  # Default: New York City
    map_zoom = 10
    m = folium.Map(location=map_center, zoom_start=map_zoom)

    # Display the map in the Streamlit app
    folium_static(m)

    # Allow the user to choose a location on the map
    selected_location = st.button("Choose Location on Map")

    if selected_location:
        st.write("Please tap on the map to select a location.")
        # Get the latitude and longitude of the clicked location
        lat, lon = get_selected_location(m)
        
        if lat is not None and lon is not None:
            # Display the latitude and longitude
            st.write("Selected Location:")
            st.write(f"Latitude: {lat}, Longitude: {lon}")
            
            # Add a marker at the selected location
            folium.Marker([lat, lon], popup="Selected Location").add_to(m)
            folium_static(m)

            # Add an arrow icon to visually indicate picking action
            st.markdown('<p style="text-align: center;"><span style="font-size:20px">&#x27A4;</span></p>', unsafe_allow_html=True)
            
            # Add a button to confirm the selection
            pick_location = st.button("Pick this Location")
            if pick_location:
                st.write("Location Picked!")
                # You can do further processing with the picked location here.

    # Add search functionality
    search_query = st.text_input("Search for a location:")
    search_button = st.button("Search")

    if search_button:
        if search_query:
            geolocator = Nominatim(user_agent="location_picker")
            location = geolocator.geocode(search_query)
            if location:
                # Move the map to the searched location
                m.location = [location.latitude, location.longitude]
                folium_static(m)
                st.write("Searched Location:")
                st.write(f"Latitude: {location.latitude}, Longitude: {location.longitude}")
            else:
                st.warning("Location not found. Please try another search query.")

def get_selected_location(map):
    # Use folium click event to get the latitude and longitude of clicked location
    latlon = map.add_child(folium.ClickForMarker(popup="Selected Location")).get_name().split(',')
    # Extract latitude and longitude from latlon list if available
    if latlon:
        if len(latlon) >= 2:
            return float(latlon[0]), float(latlon[1])
    return None, None

def visualization():
    st.subheader("Visualization Page")

    # Slider bars for visualization parameters
    amplitude = st.slider("Amplitude", 0.0, 10.0, 1.0)
    frequency = st.slider("Frequency", 0.1, 5.0, 1.0)
    size = st.slider("Size", 10, 100, 50)
    bins = st.slider("Bins", 5, 50, 20)

    # Call visualization functions with slider values
    show_line_plot(amplitude, frequency)
    show_scatter_plot(size)
    show_histogram(bins)

def show_line_plot(amplitude, frequency):
    # Generate sample data
    x = np.linspace(0, 10, 100)
    y = amplitude * np.sin(frequency * x)

    # Plot the line plot
    fig, ax = plt.subplots()
    ax.plot(x, y)
    ax.set_xlabel('Depth_id')
    ax.set_ylabel('T_cg')
    ax.set_title('Line Plot')
    st.pyplot(fig)

def show_scatter_plot(size):
    # Generate sample data
    x = np.random.randn(100)
    y = np.random.randn(100)

    # Plot the scatter plot
    fig, ax = plt.subplots()
    ax.scatter(x, y, s=size)
    ax.set_xlabel('Depth_id')
    ax.set_ylabel('T_cg')
    ax.set_title('Scatter Plot')
    st.pyplot(fig)

def show_histogram(bins):
    # Generate sample data
    data = np.random.randn(1000)

    # Plot the histogram
    fig, ax = plt.subplots()
    ax.hist(data, bins=bins)
    ax.set_xlabel('Value')
    ax.set_ylabel('Frequency')
    ax.set_title('Histogram')
    st.pyplot(fig)

if __name__ == "__main__":
    main()
