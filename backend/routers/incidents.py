from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel
from database import get_db
from models import Incident, IncidentType, User, District, RoadSegment

router = APIRouter()

class IncidentCreate(BaseModel):
    incident_type: IncidentType
    description: str
    latitude: float
    longitude: float
    district_id: Optional[int] = None
    severity: str
    photo_url: Optional[str] = None

class IncidentResponse(BaseModel):
    id: int
    incident_type: str
    description: str
    latitude: float
    longitude: float
    severity: str
    is_verified: bool
    reported_at: datetime
    photo_url: Optional[str] = None

@router.post("/report", response_model=IncidentResponse)
async def report_incident(incident: IncidentCreate, db: Session = Depends(get_db)):
    # Create new incident
    new_incident = Incident(
        incident_type=incident.incident_type,
        description=incident.description,
        latitude=incident.latitude,
        longitude=incident.longitude,
        district_id=incident.district_id,
        severity=incident.severity,
        photo_url=incident.photo_url,
        is_verified=False
    )
    
    db.add(new_incident)
    db.commit()
    db.refresh(new_incident)
    
    return new_incident

@router.get("/", response_model=List[IncidentResponse])
async def get_incidents(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    incidents = db.query(Incident).offset(skip).limit(limit).all()
    return incidents

@router.get("/{incident_id}", response_model=IncidentResponse)
async def get_incident(incident_id: int, db: Session = Depends(get_db)):
    incident = db.query(Incident).filter(Incident.id == incident_id).first()
    if not incident:
        raise HTTPException(status_code=404, detail="Incident not found")
    return incident

@router.patch("/{incident_id}/verify")
async def verify_incident(incident_id: int, db: Session = Depends(get_db)):
    incident = db.query(Incident).filter(Incident.id == incident_id).first()
    if not incident:
        raise HTTPException(status_code=404, detail="Incident not found")
    
    incident.is_verified = True
    incident.verified_at = datetime.utcnow()
    db.commit()
    
    return {"message": "Incident verified successfully", "incident_id": incident_id}
