from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Optional
from database import get_db
from models import RoadSegment, RiskCategory

router = APIRouter()

class RiskPredictionRequest(BaseModel):
    rainfall_mm: float
    slope_degree: float
    historical_incident_count: int
    road_age_years: int
    road_condition_score: Optional[float] = 50.0

class RiskPredictionResponse(BaseModel):
    risk_score: float
    risk_category: str
    confidence: float
    feature_importance: dict

@router.post("/predict-risk", response_model=RiskPredictionResponse)
async def predict_risk(request: RiskPredictionRequest, db: Session = Depends(get_db)):
    """
    Predict road risk using ML model or rule-based fallback.
    For MVP, uses a weighted rule-based approach.
    """
    # Rule-based risk calculation (MVP approach)
    # In production, this would use a trained Random Forest model
    
    # Normalize inputs
    rainfall_normalized = min(request.rainfall_mm / 200.0, 1.0)  # Normalize to 0-1
    slope_normalized = min(request.slope_degree / 45.0, 1.0)    # Normalize to 0-1
    incidents_normalized = min(request.historical_incident_count / 10.0, 1.0)
    age_normalized = min(request.road_age_years / 20.0, 1.0)
    condition_normalized = (100 - request.road_condition_score) / 100.0  # Lower score = higher risk
    
    # Weighted risk calculation
    weights = {
        'rainfall': 0.3,
        'slope': 0.25,
        'incidents': 0.25,
        'age': 0.1,
        'condition': 0.1
    }
    
    risk_score = (
        rainfall_normalized * weights['rainfall'] +
        slope_normalized * weights['slope'] +
        incidents_normalized * weights['incidents'] +
        age_normalized * weights['age'] +
        condition_normalized * weights['condition']
    ) * 100
    
    # Determine risk category
    if risk_score >= 70:
        risk_category = RiskCategory.HIGH.value
    elif risk_score >= 40:
        risk_category = RiskCategory.MEDIUM.value
    else:
        risk_category = RiskCategory.LOW.value
    
    # Feature importance (simulated for MVP)
    feature_importance = {
        'rainfall_mm': weights['rainfall'] * 100,
        'slope_degree': weights['slope'] * 100,
        'historical_incident_count': weights['incidents'] * 100,
        'road_age_years': weights['age'] * 100,
        'road_condition_score': weights['condition'] * 100
    }
    
    return RiskPredictionResponse(
        risk_score=round(risk_score, 2),
        risk_category=risk_category,
        confidence=0.85,  # Simulated confidence
        feature_importance=feature_importance
    )

@router.get("/model-info")
async def get_model_info():
    return {
        "model_type": "Rule-based fallback (MVP)",
        "features": ["rainfall_mm", "slope_degree", "historical_incident_count", "road_age_years", "road_condition_score"],
        "output": "risk_score (0-100)",
        "categories": ["low", "medium", "high"],
        "note": "Production version will use Random Forest classifier with training data"
    }
