# Import necessary libraries
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import numpy as np
import pickle
import uvicorn
import os
from fastapi.responses import HTMLResponse
import pandas as pd

# Load the saved model at startup
try:
    with open("random_forest_model.pkl", "rb") as file:
        model = pickle.load(file)
except FileNotFoundError:
    raise RuntimeError("The model file 'random_forest_model.pkl' was not found. Ensure it exists in the working directory.")

# Initialize FastAPI app
app = FastAPI(
    title="Unemployment Rate Prediction API",
    description="API for predicting unemployment rate based on economic indicators",
    version="1.0"
)

# Define input data model
class Indicators(BaseModel):
    cpi: float
    gdp: float

# Prediction endpoint
@app.post("/predict")
async def predict_unemployment_rate(indicators: Indicators):
    # Create DataFrame with the same column names used during model training
    input_data = pd.DataFrame({
        "CPI Value": [indicators.cpi],
        "GDP value": [indicators.gdp]
    })
    
    # Validate if the model has predict method
    if not hasattr(model, 'predict'):
        raise HTTPException(status_code=500, detail="Model is not capable of predictions.")
    
    # Predict unemployment rate
    prediction = model.predict(input_data)[0]
    return {"predicted_unemployment_rate": round(prediction, 2)}

# Root endpoint to render the HTML page
@app.get("/", response_class=HTMLResponse)
async def read_root():
    try:
        with open("unemploy.html", "r") as f:
            content = f.read()
        return HTMLResponse(content=content)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="HTML file 'unemploy.html' not found.")

# Run the app if this script is run directly
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
