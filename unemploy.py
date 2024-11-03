from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pickle
import numpy as np

# Load the trained Random Forest model
try:
    with open('random_forest_model.pkl', 'rb') as file:
        model = pickle.load(file)

    # Check if the model has a predict method
    if not hasattr(model, 'predict'):
        raise ValueError("Loaded model does not have a 'predict' method.")
except Exception as e:
    print(f"Error loading model: {e}")
    model = None  # Handle the case where the model fails to load

# Create a FastAPI instance
app = FastAPI()

# Allow CORS for frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update this to your frontend URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define request body model
class PredictionRequest(BaseModel):
    cpi: float
    gdp: float

# Define response model
class PredictionResponse(BaseModel):
    prediction: float

# Prediction endpoint
@app.post("/predict", response_model=PredictionResponse)
async def predict(request: PredictionRequest):
    if model is None:
        return PredictionResponse(prediction=0)  # Fallback in case the model isn't loaded

    # Prepare the input data for the model
    input_data = np.array([[request.cpi, request.gdp]])
    # Make prediction
    prediction = model.predict(input_data)
    return PredictionResponse(prediction=prediction[0])

# Root endpoint to render the HTML page
@app.get("/", response_class=HTMLResponse)
async def read_root():
    try:
        with open("unemploy.html", "r") as f:
            content = f.read()
        return HTMLResponse(content=content)
    except Exception as e:
        return HTMLResponse(content=f"Error loading HTML: {e}", status_code=500)

# To run the application, use the command: uvicorn main:app --reload
