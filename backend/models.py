from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, Text, ForeignKey, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from database import Base

class UserRole(str, enum.Enum):
    ADMIN = "admin"
    FIELD_OFFICER = "field_officer"
    TRANSPORTER = "transporter"
    CITIZEN = "citizen"

class IncidentType(str, enum.Enum):
    LANDSLIDE = "landslide"
    FLOOD = "flood"
    BRIDGE_DAMAGE = "bridge_damage"
    ROAD_BLOCKAGE = "road_blockage"
    TRAFFIC = "traffic"

class RiskCategory(str, enum.Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    role = Column(Enum(UserRole), default=UserRole.CITIZEN)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class District(Base):
    __tablename__ = "districts"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    state = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)
    risk_score = Column(Float, default=0.0)
    risk_category = Column(Enum(RiskCategory), default=RiskCategory.LOW)
    created_at = Column(DateTime, default=datetime.utcnow)

class RoadSegment(Base):
    __tablename__ = "road_segments"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    district_id = Column(Integer, ForeignKey("districts.id"))
    start_lat = Column(Float)
    start_lon = Column(Float)
    end_lat = Column(Float)
    end_lon = Column(Float)
    length_km = Column(Float)
    risk_score = Column(Float, default=0.0)
    risk_category = Column(Enum(RiskCategory), default=RiskCategory.LOW)
    rainfall_mm = Column(Float, default=0.0)
    slope_degree = Column(Float, default=0.0)
    historical_incident_count = Column(Integer, default=0)
    road_age_years = Column(Integer, default=0)
    is_blocked = Column(Boolean, default=False)
    last_updated = Column(DateTime, default=datetime.utcnow)
    
    district = relationship("District")

class Incident(Base):
    __tablename__ = "incidents"
    
    id = Column(Integer, primary_key=True, index=True)
    incident_type = Column(Enum(IncidentType))
    description = Column(Text)
    latitude = Column(Float)
    longitude = Column(Float)
    district_id = Column(Integer, ForeignKey("districts.id"))
    road_segment_id = Column(Integer, ForeignKey("road_segments.id"))
    severity = Column(String)  # low, medium, high
    reported_by = Column(Integer, ForeignKey("users.id"))
    is_verified = Column(Boolean, default=False)
    verified_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    photo_url = Column(String, nullable=True)
    reported_at = Column(DateTime, default=datetime.utcnow)
    verified_at = Column(DateTime, nullable=True)
    
    district = relationship("District")
    road_segment = relationship("RoadSegment")

class Vehicle(Base):
    __tablename__ = "vehicles"
    
    id = Column(Integer, primary_key=True, index=True)
    vehicle_id = Column(String, unique=True)
    cargo_type = Column(String)  # medicine, food, agricultural, construction
    current_lat = Column(Float)
    current_lon = Column(Float)
    destination_lat = Column(Float)
    destination_lon = Column(Float)
    route_id = Column(String, nullable=True)
    status = Column(String, default="active")  # active, delayed, arrived
    eta_minutes = Column(Integer, nullable=True)
    route_risk_score = Column(Float, default=0.0)
    last_updated = Column(DateTime, default=datetime.utcnow)

class Alert(Base):
    __tablename__ = "alerts"
    
    id = Column(Integer, primary_key=True, index=True)
    severity = Column(String)  # low, medium, high
    district_id = Column(Integer, ForeignKey("districts.id"), nullable=True)
    road_segment_id = Column(Integer, ForeignKey("road_segments.id"), nullable=True)
    message = Column(Text)
    language = Column(String, default="en")  # en, hi
    target_role = Column(Enum(UserRole), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Boolean, default=True)
    
    district = relationship("District")
    road_segment = relationship("RoadSegment")
