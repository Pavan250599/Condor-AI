import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import numpy as np


# Initialize the FastAPI app
app = FastAPI()

# Load the trained ML model
model = joblib.load("/workspaces/codespaces-jupyter/Assignment/Model/model.pkl")  # Replace with your model path

# Define the request schema using Pydantic
class InputData(BaseModel):
    Open: float
    return_pct: float
    volume_change: float
    ma_20: float
    std_20: float


@app.get("/")
def home():
    return {"message": "Welcome to the ML Model API"}

# Inference endpoint
@app.post("/predict/")
def predict(data: InputData):
    # Convert input data to numpy array
    features = np.array([[data.Open, data.return_pct, data.volume_change, data.ma_20, data.std_20]])
    
    # Get prediction from the model
    prediction = model.predict(features)

    return {"prediction": int(prediction[0])}