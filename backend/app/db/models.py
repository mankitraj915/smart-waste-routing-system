from sqlalchemy import Column, Integer, Float, String, DateTime, JSON
from datetime import datetime
from app.db.database import Base

class Bin(Base):
    __tablename__ = "bins"
    id = Column(Integer, primary_key=True, index=True)
    lat = Column(Float, nullable=False)
    lng = Column(Float, nullable=False)
    capacity_max = Column(Float, default=100.0)

class Telemetry(Base):
    __tablename__ = "telemetry"
    id = Column(Integer, primary_key=True, index=True)
    bin_id = Column(Integer, index=True)
    fill_percentage = Column(Float, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)

class DailyRoute(Base):
    __tablename__ = "daily_routes"
    id = Column(Integer, primary_key=True, index=True)
    truck_id = Column(String, index=True)
    date = Column(String, index=True) 
    route_sequence_json = Column(JSON, nullable=False)
