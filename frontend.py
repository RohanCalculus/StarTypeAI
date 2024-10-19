import streamlit as st
import requests

# API endpoint URL (replace with your actual FastAPI URL if hosted elsewhere)
api_url = "http://127.0.0.1:8000/predict/"

# Custom CSS for the background image applied to the main content area
page_bg_img = '''
<style>
[data-testid="stAppViewContainer"] {
    background-image: url("https://cdn.mos.cms.futurecdn.net/HuGGeENt6kGyixe3hT9tnY-1200-80.jpg");
    background-size: cover;
    background-repeat: no-repeat;
    background-attachment: fixed;
}

[data-testid="stAppViewContainer"] > .main {
    backdrop-filter: blur(5px);
}
</style>
'''

# Inject the background image CSS into the Streamlit app
st.markdown(page_bg_img, unsafe_allow_html=True)

# Title of the Streamlit app
st.title("Star Type Prediction")

# Instructions for the user
st.write("Enter the star's parameters to predict its type")

# Add a container with black background and white text
with st.container():
    st.markdown(
        """
        <div style='background-color: black; padding: 10px; border-radius: 10px;'>
            <p style='color: white; font-size: 16px;'>The prefilled values are for the Sun which is a Main Sequence Star.</p>
            <p>You can fill other values of any other Star and check the prediction.</p>
        </div>
        """, 
        unsafe_allow_html=True
    )

st.text("")  # Add some space between elements

# Input fields for user to enter star details
temperature = st.number_input("Temperature (K)", min_value=0, step=1, value=5770)
luminosity = st.number_input("Luminosity (L/Lo)", min_value=0.0, step=0.01, value=1.0)
radius = st.number_input("Radius (R/Ro)", min_value=0.0, step=0.01, value=1.0)
magnitude = st.number_input("Absolute magnitude (Mv)", step=0.01, value=4.83)

# Trigger prediction when button is clicked
if st.button("Predict"):
    # Prepare the payload for the API request
    payload = {
        "Temperature (K)": temperature,
        "Luminosity(L/Lo)": luminosity,
        "Radius(R/Ro)": radius,
        "Absolute magnitude(Mv)": magnitude
    }

    # Send a POST request to the FastAPI backend
    try:
        response = requests.post(api_url, json=payload)

        # Check if the request was successful
        if response.status_code == 200:
            # Parse the JSON response
            result = response.json()
            predicted_type = result.get("predicted_type")

            # Display the predicted star type
            st.success(f"Predicted Star Type: {predicted_type}")
        else:
            st.error(f"Error: Unable to get prediction. Status code {response.status_code}")
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")