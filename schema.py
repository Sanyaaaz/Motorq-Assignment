from unittest.mock import Base
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

from sqlalchemy import Column, String

class VehicleBase(BaseModel):
    vin: str
    manufacturer: str
    model: str
    fleet_id: str
    owner: str
    status: str

class VehicleCreate(VehicleBase): pass
class Vehicle(VehicleBase):
    class Config:
        orm_mode = True

class TelemetryCreate(BaseModel):
    vin: str
    latitude: float
    longitude: float
    speed: float
    engine_status: str
    fuel_level: float
    odometer: float
    diagnostic_code: Optional[str] = None
    timestamp: Optional[datetime] = None

class Telemetry(TelemetryCreate):
    id: int
    class Config:
        orm_mode = True

class Alert(BaseModel):
    id: int
    vin: str
    type: str
    severity: str
    message: str
    timestamp: datetime
    class Config:
        orm_mode = True

class DiagnosticCode(Base):
    __tablename__ = "diagnosticscode"
    code = Column(String, primary_key=True)
    description = Column(String)
    severity = Column(String)  
