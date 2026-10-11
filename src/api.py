
from pathlib import Path

import joblib
import pandas as pd
from fastapi import FastAPI
from pydantic import BaseModel, Field


# Locate the saved pipeline in the repository root.
PROJECT_ROOT = Path(__file__).resolve().parent.parent
MODEL_PATH = PROJECT_ROOT / "shopsense_pipeline.joblib"

THRESHOLD = 0.37

app = FastAPI(
    title="ShopSense API",
    description=(
        "Predict purchase intention from an online "
        "shopping session."
    ),
    version="1.0.0",
)

# Load the fitted preprocessing and model pipeline.
model = joblib.load(MODEL_PATH)


class SessionFeatures(BaseModel):
    Administrative: int = Field(ge=0)
    Administrative_Duration: float = Field(ge=0)
    Informational: int = Field(ge=0)
    Informational_Duration: float = Field(ge=0)
    ProductRelated: int = Field(ge=0)
    ProductRelated_Duration: float = Field(ge=0)
    BounceRates: float = Field(ge=0, le=1)
    ExitRates: float = Field(ge=0, le=1)
    PageValues: float = Field(ge=0)
    SpecialDay: float = Field(ge=0, le=1)

    Month: str
    OperatingSystems: int
    Browser: int
    Region: int
    TrafficType: int
    VisitorType: str
    Weekend: bool


@app.get("/")
def root():
    return {"message": "Welcome to the ShopSense API"}


@app.get("/health")
def health():
    return {"status": "ok", "model_loaded": model is not None}


@app.post("/predict")
def predict(features: SessionFeatures):
    # Preserve the feature order used during model training.
    input_data = pd.DataFrame(
        [features.model_dump()]
    )

    probability = float(
        model.predict_proba(input_data)[0, 1]
    )

    prediction = int(probability >= THRESHOLD)

    return {
        "purchase_probability": round(probability, 4),
        "predicted_purchase": prediction,
        "decision_threshold": THRESHOLD,
    }
