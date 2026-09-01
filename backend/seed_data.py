from sqlalchemy.orm import Session
from database import SessionLocal, engine, Base
from models import District, RoadSegment, Incident, Vehicle, Alert, User, UserRole, IncidentType, RiskCategory
import hashlib
import random

def seed_database():
    # Create tables
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    
    try:
        # Seed Districts (NER sample districts)
        districts_data = [
            {"name": "Kamrup", "state": "Assam", "latitude": 26.15, "longitude": 91.75},
            {"name": "Shillong", "state": "Meghalaya", "latitude": 25.57, "longitude": 91.88},
            {"name": "Imphal", "state": "Manipur", "latitude": 24.82, "longitude": 93.94},
            {"name": "Guwahati", "state": "Assam", "latitude": 26.14, "longitude": 91.73},
        ]
        
        districts = []
        for district_data in districts_data:
            district = District(**district_data)
            db.add(district)
            districts.append(district)
        
        db.commit()
        
        # Refresh to get IDs
        for district in districts:
            db.refresh(district)
        
        # Seed Road Segments
        road_segments_data = [
            {
                "name": "NH-37 Kamrup to Guwahati",
                "district_id": districts[0].id,
                "start_lat": 26.16, "start_lon": 91.76,
                "end_lat": 26.14, "end_lon": 91.73,
                "length_km": 25.5,
                "rainfall_mm": 45.2,
                "slope_degree": 5.3,
                "historical_incident_count": 2,
                "road_age_years": 8
            },
            {
                "name": "NH-44 Shillong to Guwahati",
                "district_id": districts[1].id,
                "start_lat": 25.58, "start_lon": 91.89,
                "end_lat": 26.14, "end_lon": 91.73,
                "length_km": 103.2,
                "rainfall_mm": 120.5,
                "slope_degree": 15.7,
                "historical_incident_count": 8,
                "road_age_years": 12
            },
            {
                "name": "NH-2 Imphal to Dimapur",
                "district_id": districts[2].id,
                "start_lat": 24.83, "start_lon": 93.95,
                "end_lat": 25.92, "end_lon": 93.73,
                "length_km": 78.4,
                "rainfall_mm": 85.3,
                "slope_degree": 12.4,
                "historical_incident_count": 5,
                "road_age_years": 10
            },
            {
                "name": "Internal Road Kamrup",
                "district_id": districts[0].id,
                "start_lat": 26.17, "start_lon": 91.77,
                "end_lat": 26.15, "end_lon": 91.74,
                "length_km": 15.8,
                "rainfall_mm": 30.1,
                "slope_degree": 3.2,
                "historical_incident_count": 1,
                "road_age_years": 5
            },
        ]
        
        road_segments = []
        for road_data in road_segments_data:
            road = RoadSegment(**road_data)
            # Calculate risk score
            rainfall_normalized = min(road.rainfall_mm / 200.0, 1.0)
            slope_normalized = min(road.slope_degree / 45.0, 1.0)
            incidents_normalized = min(road.historical_incident_count / 10.0, 1.0)
            age_normalized = min(road.road_age_years / 20.0, 1.0)
            
            road.risk_score = (
                rainfall_normalized * 0.3 +
                slope_normalized * 0.25 +
                incidents_normalized * 0.25 +
                age_normalized * 0.2
            ) * 100
            
            if road.risk_score >= 70:
                road.risk_category = RiskCategory.HIGH
            elif road.risk_score >= 40:
                road.risk_category = RiskCategory.MEDIUM
            else:
                road.risk_category = RiskCategory.LOW
            
            db.add(road)
            road_segments.append(road)
        
        db.commit()
        
        # Seed Users
        users_data = [
            {"username": "admin", "email": "admin@sih26002.com", "password": "admin123", "role": UserRole.ADMIN},
            {"username": "officer1", "email": "officer@sih26002.com", "password": "officer123", "role": UserRole.FIELD_OFFICER},
            {"username": "transporter1", "email": "transporter@sih26002.com", "password": "transporter123", "role": UserRole.TRANSPORTER},
            {"username": "citizen1", "email": "citizen@sih26002.com", "password": "citizen123", "role": UserRole.CITIZEN},
        ]
        
        for user_data in users_data:
            # Simple SHA256 hashing for prototype
            password = user_data["password"]
            hashed_password = hashlib.sha256(password.encode()).hexdigest()
            user = User(
                username=user_data["username"],
                email=user_data["email"],
                hashed_password=hashed_password,
                role=user_data["role"]
            )
            db.add(user)
        
        db.commit()
        
        # Seed Vehicles
        vehicles_data = [
            {
                "vehicle_id": "VEH-001",
                "cargo_type": "medicine",
                "current_lat": 26.15, "current_lon": 91.75,
                "destination_lat": 26.14, "destination_lon": 91.73,
                "status": "active",
                "eta_minutes": 45
            },
            {
                "vehicle_id": "VEH-002",
                "cargo_type": "food",
                "current_lat": 25.57, "current_lon": 91.88,
                "destination_lat": 26.14, "destination_lon": 91.73,
                "status": "active",
                "eta_minutes": 120
            },
            {
                "vehicle_id": "VEH-003",
                "cargo_type": "agricultural",
                "current_lat": 24.82, "current_lon": 93.94,
                "destination_lat": 25.92, "destination_lon": 93.73,
                "status": "active",
                "eta_minutes": 90
            },
        ]
        
        for vehicle_data in vehicles_data:
            vehicle = Vehicle(**vehicle_data)
            db.add(vehicle)
        
        db.commit()
        
        # Seed Sample Incidents
        incidents_data = [
            {
                "incident_type": IncidentType.LANDSLIDE,
                "description": "Minor landslide reported on NH-44 near Shillong",
                "latitude": 25.60, "longitude": 91.90,
                "district_id": districts[1].id,
                "road_segment_id": road_segments[1].id,
                "severity": "medium",
                "is_verified": True
            },
            {
                "incident_type": IncidentType.FLOOD,
                "description": "Water logging on NH-37 Kamrup",
                "latitude": 26.15, "longitude": 91.75,
                "district_id": districts[0].id,
                "road_segment_id": road_segments[0].id,
                "severity": "low",
                "is_verified": True
            },
        ]
        
        for incident_data in incidents_data:
            incident = Incident(**incident_data)
            db.add(incident)
        
        db.commit()
        
        # Seed Sample Alerts
        alerts_data = [
            {
                "severity": "high",
                "district_id": districts[1].id,
                "road_segment_id": road_segments[1].id,
                "message": "High risk alert: NH-44 Shillong to Guwahati - Use alternate route",
                "language": "en"
            },
            {
                "severity": "medium",
                "district_id": districts[0].id,
                "message": "Medium risk alert: Kamrup district - Monitor road conditions",
                "language": "en"
            },
        ]
        
        for alert_data in alerts_data:
            alert = Alert(**alert_data)
            db.add(alert)
        
        db.commit()
        
        print("Database seeded successfully!")
        print(f"Created {len(districts)} districts")
        print(f"Created {len(road_segments)} road segments")
        print(f"Created {len(users_data)} users")
        print(f"Created {len(vehicles_data)} vehicles")
        print(f"Created {len(incidents_data)} incidents")
        print(f"Created {len(alerts_data)} alerts")
        
    except Exception as e:
        print(f"Error seeding database: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_database()
