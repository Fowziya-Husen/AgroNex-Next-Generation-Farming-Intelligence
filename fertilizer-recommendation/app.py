import streamlit as st
import pandas as pd
import pickle
import base64

def set_bg(image_file):
    with open(image_file, "rb") as image:
        encoded = base64.b64encode(image.read()).decode()
    css = f"""
    <style>
    .stApp {{
        background-image: url("data:image/jpg;base64,{encoded}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)


import os

def set_bg(image_file):
    image_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        image_file
    )

    with open(image_path, "rb") as image:
        encoded = base64.b64encode(image.read()).decode()

    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/jpeg;base64,{encoded}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )


# Call it before title
set_bg("bg1.jpeg")


# Load model and encoders


import os
import pickle

# Get the directory containing app.py
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Define the model folder
MODEL_DIR = os.path.join(BASE_DIR, "model")

# Function to load pickle files
def load_pickle(filename):
    file_path = os.path.join(MODEL_DIR, filename)

    with open(file_path, "rb") as file:
        return pickle.load(file)

# Load the fertilizer prediction model
model = load_pickle("fertilizer_model.pkl")

# Load encoders
soil_encoder = load_pickle("soil_encoder.pkl")
crop_encoder = load_pickle("crop_encoder.pkl")
fertilizer_decoder = load_pickle("fert_encoder.pkl")

print("Fertilizer model and all encoders loaded successfully!")


# Input fields
temperature = st.number_input("Temperature (°C)", min_value=0)
humidity = st.number_input("Humidity (%)", min_value=0)
moisture = st.number_input("Soil Moisture", min_value=0)
soil_type = st.selectbox("Soil Type", soil_encoder.classes_)
crop_type = st.selectbox("Crop Type", crop_encoder.classes_)
nitrogen = st.number_input("Nitrogen level", min_value=0)
potassium = st.number_input("Potassium level", min_value=0)
phosphorous = st.number_input("Phosphorous level", min_value=0)

if st.button("Get Fertilizer Recommendation"):
    # Encode inputs
    soil_encoded = soil_encoder.transform([soil_type])[0]
    crop_encoded = crop_encoder.transform([crop_type])[0]

    input_data = [[
        temperature, humidity, moisture, soil_encoded,
        crop_encoded, nitrogen, potassium, phosphorous
    ]]

    prediction = model.predict(input_data)[0]
    fertilizer = fertilizer_decoder.inverse_transform([prediction])[0]

    st.markdown(
    f"""
    <div style='
        background-color:#000000;
        padding:10px 15px;
        border-radius:10px;
        border-left: 5px solid green;
        font-weight:bold;
        font-size:16px;
    '>
        🌱 Recommended Fertilizer: <span style='color:green'>{fertilizer}</span>
    </div>
    """,
    unsafe_allow_html=True
)


