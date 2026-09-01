from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from models import District, RoadSegment, Incident, Vehicle, Alert, RiskCategory

router = APIRouter()

@router.get("/summary")
async def get_dashboard_summary(db: Session = Depends(get_db)):
    """Get overall dashboard summary statistics"""
    
    # Get counts
    total_districts = db.query(District).count()
    total_road_segments = db.query(RoadSegment).count()
    active_incidents = db.query(Incident).filter(Incident.is_verified == True).count()
    active_vehicles = db.query(Vehicle).filter(Vehicle.status == "active").count()
    active_alerts = db.query(Alert).filter(Alert.is_active == True).count()
    
    # Get risk distribution
    high_risk_roads = db.query(RoadSegment).filter(RoadSegment.risk_category == RiskCategory.HIGH).count()
    medium_risk_roads = db.query(RoadSegment).filter(RoadSegment.risk_category == RiskCategory.MEDIUM).count()
    low_risk_roads = db.query(RoadSegment).filter(RoadSegment.risk_category == RiskCategory.LOW).count()
    
    # Get blocked roads
    blocked_roads = db.query(RoadSegment).filter(RoadSegment.is_blocked == True).count()
    
    return {
        "overview": {
            "total_districts": total_districts,
            "total_road_segments": total_road_segments,
            "active_incidents": active_incidents,
            "active_vehicles": active_vehicles,
            "active_alerts": active_alerts
        },
        "risk_distribution": {
            "high": high_risk_roads,
            "medium": medium_risk_roads,
            "low": low_risk_roads
        },
        "road_status": {
            "blocked": blocked_roads,
            "clear": total_road_segments - blocked_roads
        }
    }

@router.get("/recent-incidents")
async def get_recent_incidents(limit: int = 10, db: Session = Depends(get_db)):
    """Get recent verified incidents"""
    incidents = db.query(Incident).filter(Incident.is_verified == True).order_by(Incident.reported_at.desc()).limit(limit).all()
    
    return [
        {
            "id": incident.id,
            "type": incident.incident_type.value,
            "description": incident.description,
            "severity": incident.severity,
            "latitude": incident.latitude,
            "longitude": incident.longitude,
            "reported_at": incident.reported_at
        } for incident in incidents
    ]

@router.get("/high-risk-roads")
async def get_high_risk_roads(limit: int = 20, db: Session = Depends(get_db)):
    """Get roads with high risk scores"""
    roads = db.query(RoadSegment).filter(
        RoadSegment.risk_category == RiskCategory.HIGH
    ).order_by(RoadSegment.risk_score.desc()).limit(limit).all()
    
    return [
        {
            "id": road.id,
            "name": road.name,
            "district_id": road.district_id,
            "risk_score": road.risk_score,
            "risk_category": road.risk_category.value,
            "is_blocked": road.is_blocked,
            "rainfall_mm": road.rainfall_mm,
            "slope_degree": road.slope_degree
        } for road in roads
    ]
