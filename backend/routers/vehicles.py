from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from pydantic import BaseModel
from database import get_db
from models import Vehicle

router = APIRouter()

class VehicleResponse(BaseModel):
    id: int
    vehicle_id: str
    cargo_type: str
    current_lat: float
    current_lon: float
    status: str
    eta_minutes: int
    route_risk_score: float

@router.get("/", response_model=List[VehicleResponse])
async def get_vehicles(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    vehicles = db.query(Vehicle).offset(skip).limit(limit).all()
    return vehicles

@router.get("/{vehicle_id}", response_model=VehicleResponse)
async def get_vehicle(vehicle_id: str, db: Session = Depends(get_db)):
    vehicle = db.query(Vehicle).filter(Vehicle.vehicle_id == vehicle_id).first()
    if not vehicle:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    return vehicle

@router.get("/{vehicle_id}/track")
async def track_vehicle(vehicle_id: str, db: Session = Depends(get_db)):
    vehicle = db.query(Vehicle).filter(Vehicle.vehicle_id == vehicle_id).first()
    if not vehicle:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    
    return {
        "vehicle_id": vehicle.vehicle_id,
        "cargo_type": vehicle.cargo_type,
        "current_position": {
            "lat": vehicle.current_lat,
            "lon": vehicle.current_lon
        },
        "destination": {
            "lat": vehicle.destination_lat,
            "lon": vehicle.destination_lon
        },
        "status": vehicle.status,
        "eta_minutes": vehicle.eta_minutes,
        "route_risk_score": vehicle.route_risk_score,
        "last_updated": vehicle.last_updated
    }
