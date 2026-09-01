from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from pydantic import BaseModel
from database import get_db
from models import Alert, UserRole

router = APIRouter()

class AlertCreate(BaseModel):
    severity: str
    district_id: int = None
    road_segment_id: int = None
    message: str
    language: str = "en"
    target_role: UserRole = None

class AlertResponse(BaseModel):
    id: int
    severity: str
    message: str
    language: str
    is_active: bool

@router.post("/broadcast")
async def broadcast_alert(alert: AlertCreate, db: Session = Depends(get_db)):
    new_alert = Alert(
        severity=alert.severity,
        district_id=alert.district_id,
        road_segment_id=alert.road_segment_id,
        message=alert.message,
        language=alert.language,
        target_role=alert.target_role
    )
    
    db.add(new_alert)
    db.commit()
    db.refresh(new_alert)
    
    return {"message": "Alert broadcast successfully", "alert_id": new_alert.id}

@router.get("/", response_model=List[AlertResponse])
async def get_alerts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    alerts = db.query(Alert).filter(Alert.is_active == True).offset(skip).limit(limit).all()
    return alerts

@router.get("/{alert_id}")
async def get_alert(alert_id: int, db: Session = Depends(get_db)):
    alert = db.query(Alert).filter(Alert.id == alert_id).first()
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")
    return alert
