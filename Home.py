import streamlit as st
import pandas as pd
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

# Create Streamlit app interface
def main():
    st.title('Fishing Prediction')

    # Input fields
    depthm = st.number_input('Depth (m)', min_value=0.0, step=1.0)
    T_degC = st.number_input('Temperature (°C)')
    Salnty = st.number_input('Salinity')
    O2ml_L = st.number_input('Oxygen (ml/L)')
    STheta = st.number_input('Sigma-theta')
    O2Sat = st.number_input('Oxygen Saturation (%)')
    Oxy_µmol_Kg = st.number_input('Oxygen (µmol/Kg)')

    # Prediction button
    if st.button('Predict Fishing'):
        prediction = predict_temperature(depthm, T_degC, Salnty, O2ml_L, STheta, O2Sat, Oxy_µmol_Kg)
        st.write('Fishing is Not Good!' if prediction[0] else 'Fishing is Perfect!')

if __name__ == '__main__':
    main()
