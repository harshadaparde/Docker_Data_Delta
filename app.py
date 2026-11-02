import joblib
from pathlib import Path
from fastapi import FastAPI
from pydantic import BaseModel,Field 
BASE_DIR=Path(__file__).parent
MODEL_PATH=BASE_DIR/"model.joblib"
model=joblib.load(MODEL_PATH)
# create fastapi application
app=FastAPI(
    title="Student Performance Prediction API",
    description="Predict an expected score from study hours",
    version="1.0.0"
    
)
class StudentInput(BaseModel):
    study_hours:float=Field(ge=0,le=10)

@app.get("/")
def home():
    return{
        "message":"Student Performanc API is running"
    }  

@app.get("/health")
def health():
    return{"Status":"healthy"}

@app.post("/predict")
def predict(data: StudentInput):
    print("Received data:", data)

    prediction = model.predict([[data.study_hours]])[0]
    prediction = max(0.0, min(100.0, float(prediction)))

    return {
        "study_hours": data.study_hours,
        "predicted_score": round(prediction, 2)
    }
    
      
    
