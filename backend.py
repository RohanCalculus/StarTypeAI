from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import pandas as pd
from joblib import load

# Initialize FastAPI app
app = FastAPI()

# Specify your Streamlit app's URL (replace with the actual URL where your Streamlit app is hosted)
streamlit_app_origin = "http://localhost:8501"  # Update this with your Streamlit app URL

# Add CORS middleware to allow only requests from your Streamlit app and allow all methods and headers
app.add_middleware(
    CORSMiddleware,
    allow_origins=[streamlit_app_origin],  # Only allow the Streamlit app to access the API
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"]  # Allow all headers
)

# Load the pre-trained machine learning pipeline using joblib
pipeline = load('pipeline/pipeline_star_type_pred.joblib')


class StarDetails(BaseModel):
    """
    Pydantic model for validating the input data for star characteristics.
    """
    temperature: int = Field(..., alias="Temperature (K)", description="Temperature of the star in Kelvin")
    luminosity: float = Field(..., alias="Luminosity(L/Lo)", description="Luminosity of the star relative to the sun")
    radius: float = Field(..., alias="Radius(R/Ro)", description="Radius of the star relative to the sun")
    magnitude: float = Field(..., alias="Absolute magnitude(Mv)", description="Absolute magnitude of the star")


@app.get("/")
def root():
    """
    Health check endpoint to confirm that the API is running.
    """
    return {"message": "Star Type Prediction API is running"}


@app.post("/predict/")
def predict_star_type(star: StarDetails):
    """
    Endpoint to predict the star type based on input characteristics.
    """
    # Prepare the input data as a dictionary to match the format expected by the model
    star_dict = {
        'Temperature (K)': star.temperature,
        'Luminosity(L/Lo)': star.luminosity,
        'Radius(R/Ro)': star.radius,
        'Absolute magnitude(Mv)': star.magnitude
    }

    # Convert the dictionary to a Pandas DataFrame
    test_df = pd.DataFrame(star_dict, index=[0])

    # Predict the star type using the pre-trained machine learning pipeline
    y_pred = pipeline.predict(test_df)[0]

    # Return the prediction as a JSON object
    return {
        "predicted_type": y_pred
    }
