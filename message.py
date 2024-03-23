import streamlit as st
import folium
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
from streamlit_folium import folium_static
from geopy.geocoders import Nominatim
import pickle
from twilio.rest import Client

# Load the pre-trained model
with open('model.pickle', 'rb') as f:
    model = pickle.load(f)

import os
TWILIO_ACCOUNT_SID = os.getenv('ACee990bc578ce1c94881c415c452204a7')
TWILIO_AUTH_TOKEN = os.getenv('b775e51b5790f80bca674ac4fcb84742')
TWILIO_PHONE_NUMBER = os.getenv('+15642346746')

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

def send_sms(phone_number, message):
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    message = client.messages.create(
        body=message,
        from_=TWILIO_PHONE_NUMBER,
        to=phone_number
    )
    return message.sid

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
        message = 'Fishing is Not Good!' if prediction[0] else 'Fishing is Perfect!'
        st.write(message)
        send_sms(phone_number, message)
        if(prediction[0]):
            st.button('alert')
        else:
            st.button('safe')

home()
