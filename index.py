import streamlit as st
import pandas as pd
import pickle
import random
import time
from datetime import datetime, timedelta
import pytz 
# Set a custom page configuration
st.set_page_config(
    page_title="Food Delivery Time Prediction",
    page_icon="🍔",
    layout="centered",
    initial_sidebar_state="expanded",
)

# Background style and customizations
st.markdown(
    """
    <style>
    [data-testid="stAppViewContainer"] {
        background-color: #121212;
        color: white;
    }
    [data-testid="stSidebar"] {
        background-color: #1f1f1f;
    }
    .stButton>button {
        background-color: #4caf50;
        color: white;
        font-size: 18px;
        border-radius: 5px;
        width: 100%;
        height: 50px;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #45a049;
        transform: scale(1.05);
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# App header
st.image("food.jpeg")
st.title("🚀 Food Delivery Time Prediction")
st.subheader("Predict how long your food delivery will take based on various factors.")

# Fun facts about food delivery
fun_facts = [
    "Did you know? The world's longest food delivery took 1 hour 45 minutes!",
    "Fun fact: The fastest delivery time recorded was under 10 minutes!",
    "Delivery times can be affected by weather, traffic, and even the type of vehicle used.",
    "In some countries, delivery riders travel by bicycles for quicker delivery."
]

# Interactive inputs in cards
with st.form("prediction_form"):
    st.header("Enter Delivery Details:")

    # Input fields within cards
    st.markdown("### 🚗 Traffic & Weather")
    weather = st.selectbox("Weather Conditions", ['Windy', 'Clear', 'Foggy', 'Rainy', 'Snowy'])
    traffic_level = st.selectbox("Traffic Level", ['Low', 'Medium', 'High'])

    st.markdown("### 🛵 Vehicle & Delivery Time")
    vehicle_type = st.radio("Vehicle Type", ['Scooter', 'Bike', 'Car'], horizontal=True)
    Distance = st.slider("Trip Distance (in km)", min_value=1, max_value=50, value=10)

    preparation_time = st.number_input("Preparation Time (in minutes)", min_value=1, max_value=120, value=20)
    Courier_Experience = st.slider("Courier Experience (in years)", min_value=0, max_value=20, value=2)
    time_of_Day = st.selectbox("Time of Day", ['Afternoon', 'Evening', 'Night', 'Morning'])

    submit = st.form_submit_button("Predict Delivery Time")

# Process input and make prediction
if submit:
    # Map inputs to numerical values
    weather_mapping = {'Windy': 1, 'Clear': 2, 'Foggy': 3, 'Rainy': 4, 'Snowy': 5}
    traffic_mapping = {'Low': 1, 'Medium': 2, 'High': 3}
    time_of_day_mapping = {'Morning': 1, 'Afternoon': 2, 'Evening': 3, 'Night': 4}
    vehicle_mapping = {'Scooter': 1, 'Bike': 2, 'Car': 3}

    # Create DataFrame for prediction
    prediction_data = pd.DataFrame({
        'Distance_km': [Distance],
        'Weather': [weather_mapping[weather]],
        'Traffic_Level': [traffic_mapping[traffic_level]],
        'Time_of_Day': [time_of_day_mapping[time_of_Day]],
        'Vehicle_Type': [vehicle_mapping[vehicle_type]],
        'Preparation_Time_min': [preparation_time],
        'Courier_Experience_yrs': [Courier_Experience]
    })

    # Show a progress bar while processing the prediction
    progress = st.progress(0)
    for i in range(100):
        time.sleep(0.02)  # Simulate a delay
        progress.progress(i + 1)

    # Show the loading spinner during the prediction process
    with st.spinner("Making your prediction..."):
        try:
            # Load the model and make a prediction
            with open('modellinear.pkl', 'rb') as file:
                model = pickle.load(file)
            prediction = model.predict(prediction_data)
            prediction_value = round(float(prediction[0]))

            # Display the prediction
            st.success("Prediction Complete!")
            st.markdown(
                f"<h2 style='text-align: center; color: #0073e6;'>🚚 Estimated Delivery Time: {prediction_value} minutes</h2>",
                unsafe_allow_html=True,
            )

            # Calculate real-time delivery completion time
            ist = pytz.timezone("Asia/Kolkata")
            current_time = datetime.now(ist)  # localized time
            delivery_time = current_time + timedelta(minutes=prediction_value)
            formatted_delivery_time = delivery_time.strftime("%I:%M %p")

            st.markdown(
            f"<h3 style='text-align: center; color: #4caf50;'>📅 Your Order is Expected at: {formatted_delivery_time}</h3>",
            unsafe_allow_html=True,
)

        except FileNotFoundError:
            st.error("Model file not found. Please upload 'modellinear.pkl' in the current directory.")
        except Exception as e:
            st.error(f"An error occurred: {e}")

        # Provide feedback based on weather and traffic conditions
        if traffic_level == 'High':
            st.warning("⚠ Traffic is high. Your order may be delayed.")
        elif traffic_level == 'Medium':
            st.info("🚗 Traffic is moderate. Delivery might take a bit longer.")
        else:
            st.success("🚚 Traffic is low. Your delivery should be quick!")

        if weather in ['Rainy', 'Snowy']:
            st.warning("⚠ Bad weather (rain/snow) might cause delays in delivery.")
        elif weather == 'Foggy':
            st.info("🌫 Foggy conditions could lead to slightly longer delivery times.")
        else:
            st.success("☀ Clear weather means smooth delivery conditions!")

        # Fun fact display
        random_fact = random.choice(fun_facts)
        fact_heading = "Did you know?"
        st.subheader(fact_heading)
        st.write(f"*Fact:* {random_fact}")

# Add footer
st.markdown(
    """
    <hr style="border:1px solid #ddd;">
    <p style="text-align: center;">Created with ❤ using Streamlit</p>
    """,
    unsafe_allow_html=True,
)
