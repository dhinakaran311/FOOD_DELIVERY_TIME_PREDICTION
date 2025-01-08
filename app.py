import streamlit as st  # Importing the Streamlit library for building the web app
import pandas as pd  # Importing pandas for creating and managing dataframes
import pickle  # Importing pickle for loading the pre-trained model

# Display an image at the top of the app
st.image('food.png', use_column_width=False)

# Title of the application
st.title("Food Delivery Time Prediction")

# User input for distance in kilometers
Distance = st.number_input("Enter the Distance")

# User input for weather conditions
weather = st.radio("Pick Your Weather", ['Windy', 'Clear', 'Foggy', 'Rainy', 'Snowy'])

# User input for traffic level
traffic_level = st.radio("Select the Trafiic Level", ['Low', 'Medium', 'High'])

# User input for time of day
time_of_Day = st.radio('Select the Time of day', ['Afternoon', 'Evening', 'Night', 'Morning'])

# User input for the type of vehicle
vehicle_type = st.radio('Select the vehicle Type', ['Scooter', 'Bike', 'Car'])

# User input for food preparation time in minutes
preparation_time = st.number_input("Enter the preparation time")

# User input for courier's years of experience
Courier_Experience = st.number_input("Enter the Courier experience year")

# Button to submit the form
submit = st.button("Submit")

# Load the pre-trained machine learning model
with open('modellinear.pkl', 'rb') as file:  
    model = pickle.load(file)

# If the submit button is clicked
if submit:
    # Map weather conditions to numerical values
    if weather == "Windy":
        weather = 1
    if weather == "Clear":
        weather = 2
    if weather == "Foggy":
        weather = 3
    if weather == "Rainy":
        weather = 4
    if weather == "Snowy":
        weather = 5           

    # Map traffic levels to numerical values
    if traffic_level == "Low":
        traffic_level = 1
    if traffic_level == "Medium":
        traffic_level = 2
    if traffic_level == "High":
        traffic_level = 3
    
    # Map time of day to numerical values
    if time_of_Day == "Morning":
        time_of_Day = 1
    if time_of_Day == "Afternoon":
        time_of_Day = 2
    if time_of_Day == "Evening":
        time_of_Day = 3
    if time_of_Day == "Night":
        time_of_Day = 4 

    # Map vehicle types to numerical values
    if vehicle_type == "Scooter":
        vehicle_type = 1
    if vehicle_type == "Bike":
        vehicle_type = 2
    if vehicle_type == "Car":
        vehicle_type = 3

    # Create a DataFrame with user input to feed into the model
    prediction_data = pd.DataFrame({
        'Distance_km': [Distance],
        'Weather': [weather],
        'Traffic_Level': [traffic_level],
        'Time_of_Day': [time_of_Day],
        'Vehicle_Type': [vehicle_type],
        'Preparation_Time_min': [preparation_time],
        'Courier_Experience_yrs': [Courier_Experience],
        # 'Delivery_Time_min': [time_delivery]  # Uncomment this if time delivery is required
    })
                                      
    # Make a prediction using the pre-trained model
    prediction = model.predict(prediction_data)
    prediction_value = round(float(prediction[0]))  # Round the prediction to the nearest integer

    # Display the estimated delivery time
    st.markdown(
        f"<h2 style='text-align: center; font-size: 50px;'>Estimated Delivery Time: {prediction_value} minutes</h2>", 
        unsafe_allow_html=True
    )