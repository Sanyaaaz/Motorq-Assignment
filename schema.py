from pydantic import BaseModel,validator
from typing import Optional, List
from datetime import datetime
from enum import Enum

class StatusEnum(str, Enum):
    Active = "Active"
    Maintenance = "Maintenance"
    Decommissioned = "Decommissioned"

class EngineStatus(str, Enum):
    On = "On"
    Off = "Off"
    Idle = "Idle"

class VehicleBase(BaseModel):
    vin: str
    manufacturer: str
    model: str
    fleet_id: str
    owner: str
    status: StatusEnum

    

class VehicleCreate(VehicleBase):
    pass

class Vehicle(VehicleBase):
    pass

class TelemetryCreate(BaseModel):
    vin: str
    latitude: float
    longitude: float
    speed: float
    engine_status: EngineStatus
    fuel_level: float
    odometer: float
    diagnostic_code: Optional[List[str]] = []
    timestamp: Optional[datetime] = None

    @validator("engine_status", pre=True)
    def normalize_engine_status(cls, v):
        if isinstance(v, str):
            return v.capitalize()
        return v

    class Config:
        orm_mode = True

class Telemetry(TelemetryCreate):
    id: int


class Alert(BaseModel):
    id: int
    vin: str
    type: str
    severity: str
    message: str
    timestamp: datetime

    class Config:
        orm_mode = True
