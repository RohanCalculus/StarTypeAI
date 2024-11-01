from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse
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

    # Probability output
    y_pred_prob = pipeline.predict_proba(test_df)[0].max()

    # Return the prediction as a JSON object
    return {
        "predicted_type": y_pred,
        "predicted_probability": y_pred_prob
    }

@app.post("/bulk_predict/")
async def bulk_predict(file: UploadFile = File(...)):
    """
    Endpoint for bulk prediction of star types based on input CSV file.
    """
    # Read the uploaded file as a pandas DataFrame
    input_df = pd.read_csv(file.file)

    # Define the required columns in the expected order
    required_columns = ['Temperature (K)', 'Luminosity(L/Lo)', 'Radius(R/Ro)', 'Absolute magnitude(Mv)']
    
    # Check that the CSV has all the required columns
    if not all(col in input_df.columns for col in required_columns):
        return {"error": "CSV must contain columns: Temperature (K), Luminosity(L/Lo), Radius(R/Ro), Absolute magnitude(Mv)"}

    # Reorder columns to ensure they match the expected order
    input_df = input_df[required_columns]

    # Run predictions on the reordered DataFrame
    predictions = pipeline.predict(input_df)

    # Add predictions to the DataFrame as a new column
    input_df['Predicted Type'] = predictions

    # Save the resulting DataFrame with predictions to a new CSV file
    output_file_path = "predicted_star_types.csv"
    input_df.to_csv(output_file_path, index=False)

    # Return the CSV file as a downloadable response
    return FileResponse(path=output_file_path, media_type='text/csv', filename="predicted_star_types.csv")
