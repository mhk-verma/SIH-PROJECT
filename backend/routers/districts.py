from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from pydantic import BaseModel
from database import get_db
from models import District, RoadSegment, RiskCategory

router = APIRouter()

class DistrictResponse(BaseModel):
    id: int
    name: str
    state: str
    latitude: float
    longitude: float
    risk_score: float
    risk_category: str

@router.get("/", response_model=List[DistrictResponse])
async def get_districts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    districts = db.query(District).offset(skip).limit(limit).all()
    return districts

@router.get("/{district_id}", response_model=DistrictResponse)
async def get_district(district_id: int, db: Session = Depends(get_db)):
    district = db.query(District).filter(District.id == district_id).first()
    if not district:
        raise HTTPException(status_code=404, detail="District not found")
    return district

@router.get("/{district_id}/status")
async def get_district_status(district_id: int, db: Session = Depends(get_db)):
    district = db.query(District).filter(District.id == district_id).first()
    if not district:
        raise HTTPException(status_code=404, detail="District not found")
    
    # Get road segments for this district
    road_segments = db.query(RoadSegment).filter(RoadSegment.district_id == district_id).all()
    
    # Calculate statistics
    total_roads = len(road_segments)
    blocked_roads = len([r for r in road_segments if r.is_blocked])
    high_risk_roads = len([r for r in road_segments if r.risk_category == RiskCategory.HIGH])
    
    return {
        "district": district.name,
        "state": district.state,
        "risk_score": district.risk_score,
        "risk_category": district.risk_category.value,
        "total_roads": total_roads,
        "blocked_roads": blocked_roads,
        "high_risk_roads": high_risk_roads,
        "road_segments": [
            {
                "id": r.id,
                "name": r.name,
                "risk_score": r.risk_score,
                "risk_category": r.risk_category.value,
                "is_blocked": r.is_blocked
            } for r in road_segments
        ]
    }
