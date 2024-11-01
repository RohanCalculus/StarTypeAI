import streamlit as st
import requests
import pandas as pd
from io import StringIO

# API endpoints
single_predict_url = "http://127.0.0.1:8000/predict/"
bulk_predict_url = "http://127.0.0.1:8000/bulk_predict/"

# Custom CSS for background
page_bg_img = '''
<style>
[data-testid="stAppViewContainer"] {
    background-image: url("https://images-wixmp-ed30a86b8c4ca887773594c2.wixmp.com/f/5eae36e3-278f-4731-be00-1440d36eca76/d30idy4-9a4a96ed-33be-4941-99c1-8b77adb23288.jpg?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJ1cm46YXBwOjdlMGQxODg5ODIyNjQzNzNhNWYwZDQxNWVhMGQyNmUwIiwic3ViIjoidXJuOmFwcDo3ZTBkMTg4OTgyMjY0MzczYTVmMGQ0MTVlYTBkMjZlMCIsImF1ZCI6WyJ1cm46c2VydmljZTpmaWxlLmRvd25sb2FkIl0sIm9iaiI6W1t7InBhdGgiOiIvZi81ZWFlMzZlMy0yNzhmLTQ3MzEtYmUwMC0xNDQwZDM2ZWNhNzYvZDMwaWR5NC05YTRhOTZlZC0zM2JlLTQ5NDEtOTljMS04Yjc3YWRiMjMyODguanBnIn1dXX0.urB7x7zyDCCRhro0z1HDVMWXZ9HJi9NgdXurlCon43Q");
    background-size: cover;
    background-repeat: no-repeat;
    background-attachment: fixed;
}

[data-testid="stAppViewContainer"] > .main {
    backdrop-filter: blur(5px);
}
</style>
'''

# Inject the background image CSS
st.markdown(page_bg_img, unsafe_allow_html=True)

# Title of the app
st.markdown("<h1 style='color:cyan;'>✨ Star Type Predictor 🌟</h1>", unsafe_allow_html=True)

# Page selection dropdown
page = st.selectbox("Choose a page:", ["Introduction", "Single Prediction Mode", "Bulk Prediction Mode"])

# Display Introduction Page if selected
if page == "Introduction":

    # Introduction section
    with st.container():
        st.markdown("""
        <div style='background-color: rgba(255, 235, 235, 0.8); padding: 20px; border-radius: 10px;'>
            <h3 style='color: maroon;'>Introduction to Project</h3>
            <p style='color:black;'><b>This web application is designed to help you predict the type of stars based on their physical parameters. Using machine learning models, we analyze key attributes of stars, such as <u>temperature</u>, <u>luminosity</u>, <u>radius</u>, and <u>absolute magnitude</u>, to classify them into different types.</b></p>
        </div>
        """, unsafe_allow_html=True)

    st.text(" ")

    # Importance section
    with st.container():
        st.markdown("""
        <div style='background-color: rgba(230, 230, 250, 0.8); padding: 20px; border-radius: 10px;'>
            <h3 style='color: darkblue;'>How to Use This Web Application?</h3>
            <ul style='font-size: 16px; color:black;'>
                <li>
                    <strong>Select either <u>Single Prediction Mode</u> or <u>Bulk Prediction Mode</u> from the dropdown.
                </li>
                <li>
                    <strong>Single Prediction can predict the type of a single star based on its properties.
                </li>
                <li>
                    <strong>Bulk Prediction can predict the type of multiple stars based on its properties in the csv file.
                </li>
                <li>
                    <strong>Respective page shall guide you more about how to use it.
                </li>
            </ul>
        </div>
        """, unsafe_allow_html=True)


    st.text(" ")


    # Call to action section
    with st.container():
        st.markdown("""
        <div style='background-color: rgba(200, 170, 200, 0.8); padding: 20px; border-radius: 10px;'>
            <h3 style='color: rgba(200, 20, 6, 1);'>Get Started!</h3>
            <p style='color:black;'><b>Choose either the Single or Bulk Prediction mode from the menu to start exploring the stars!</b></p>
        </div>
        """, unsafe_allow_html=True)

# Display Single Prediction Page if selected
elif page == "Single Prediction Mode":

    # Information section with black background and white text
    with st.container():
        st.markdown(
            """
            <div style='background-color: rgba(255, 205, 255, 0.8); padding: 20px; border-radius: 10px;'>
                <h3 style='color: maroon;'>Single Star Type Predictor Mode:</h3>
                <ul style='font-size: 16px; color: black;'>
                    <li>
                        <strong>Provide properties of the star to predict its type!
                    </li>
                    <li>
                        <strong>The default values are for the Sun. You can modify these to analyze other stars.
                    </li>
                    <li>
                        <strong>Click the Predict button to get the predicted star type.
                    </li>
                    <li>
                        <strong>Green (good), Yellow (ok), and Red (bad) status shows the confidence level of the model.
                    </li>
                </ul>
            </div>
            """, 
            unsafe_allow_html=True
        )

    st.text("")  # Space between elements

    # Input fields for user to enter star details
    temperature = st.number_input("Temperature (K):-", min_value=0, step=1, value=5770)
    luminosity = st.number_input("Luminosity wrt Sun (L/Lo):-", min_value=0.0, step=0.01, value=1.0)
    radius = st.number_input("Radius wrt Sun (R/Ro):-", min_value=0.0, step=0.01, value=1.0)
    magnitude = st.number_input("Absolute magnitude (Mv):-", step=0.01, value=4.83)

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
            response = requests.post(single_predict_url, json=payload)

            # Check if the request was successful
            if response.status_code == 200:
                result = response.json()
                predicted_type = result.get("predicted_type")
                probability = result.get("predicted_probability")

                # Create a dynamic container for the prediction results
                with st.container():
                    if probability >= 0.47:
                        background_color = "rgba(76, 175, 80, 0.8)"  # Green for good predictions
                        text_color = "white"
                        message = "Predicted Star Type: " + predicted_type
                    elif 0.27 <= probability < 0.47:
                        background_color = "rgba(255, 235, 59, 0.8)"  # Yellow for okayish predictions
                        text_color = "black"
                        message = "Predicted Star Type: " + predicted_type
                    else:
                        background_color = "rgba(244, 67, 54, 0.8)"  # Red for low confidence predictions
                        text_color = "white"
                        message = "Predicted Star Type: " + predicted_type

                    st.markdown(
                        f"""
                        <div style='background-color: {background_color}; padding: 10px 0px 1px 10px; border-radius: 10px;'>
                            <p style='color: {text_color};'>{message}</p>
                        </div>
                        """, 
                        unsafe_allow_html=True
                    )
                
            else:
                st.error(f"Error: Unable to get prediction. Status code {response.status_code}")
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")


# Display Bulk Prediction Page if selected
elif page == "Bulk Prediction Mode":
    
    # Container with instructions in chocolate color and 0.8 opacity
    with st.container():
        st.markdown(
            """
            <div style='background-color: rgba(189, 252, 201, 0.8); padding: 20px; border-radius: 10px; color:black;'>
                <h3 style='color: darkgreen;'>Multiple Star Type Predictor Mode</h3>
                <p style='color: black;'><b>Upload a CSV file with the following features:</b></p> 
                    <li>
                        <strong>Temperature (K)</strong>
                    </li>
                    <li> 
                        <strong>Luminosity (L/Lo)</strong>
                    </li>
                    <li>
                        <strong>Radius (R/Ro)</strong>
                    </li>
                    <li>
                        <strong>Absolute Magnitude (Mv)</strong>
                    </li>
                <p> </p>
                <p><b>The system will analyze and return a CSV file with predicted star types for each entry.</b></p>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.text(" ")

    # File uploader for CSV file
    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

    # Automatically trigger bulk prediction when a file is uploaded
    if uploaded_file is not None:
        try:
            # Send the CSV file to the FastAPI bulk_predict endpoint
            response = requests.post(
                bulk_predict_url,
                files={"file": uploaded_file.getvalue()}
            )

            # Check if the request was successful
            if response.status_code == 200:
                # Convert response to a DataFrame and display results
                output_df = pd.read_csv(StringIO(response.content.decode('utf-8')))
                st.markdown("<h4 style='color:violet;'>Predicted Results:-</h4>", unsafe_allow_html=True)
                st.dataframe(output_df)
            else:
                st.error(f"Error: Unable to get predictions. Status code {response.status_code}")
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
