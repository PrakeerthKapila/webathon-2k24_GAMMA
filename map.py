import streamlit as st
import folium
from streamlit_folium import folium_static
from geopy.geocoders import Nominatim

def main():
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

main()