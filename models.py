import enum
import json
from datetime import datetime
from sqlalchemy import Column, String, Integer, Float, DateTime, Enum, ForeignKey
from sqlalchemy.types import TypeDecorator
from database import Base

class StatusEnum(str, enum.Enum):
    Active = "Active"
    Maintenance = "Maintenance"
    Decommissioned = "Decommissioned"

class EngineStatus(str, enum.Enum):
    On = "On"
    Off = "Off"
    Idle = "Idle"

class StringList(TypeDecorator):
    impl = String

    def process_bind_param(self, value, dialect):
        if isinstance(value, list):
            return json.dumps(value)
        return "[]"

    def process_result_value(self, value, dialect):
        try:
            return json.loads(value) if value else []
        except Exception:
            return []

class Vehicle(Base):
    __tablename__ = "vehicles"

    vin = Column(String, primary_key=True, index=True)
    manufacturer = Column(String)
    model = Column(String)
    fleet_id = Column(String)
    owner = Column(String)
    status = Column(Enum(StatusEnum))

class Telemetry(Base):
    __tablename__ = "telemetry"

    id = Column(Integer, primary_key=True, index=True)
    vin = Column(String, ForeignKey("vehicles.vin"))
    latitude = Column(Float)
    longitude = Column(Float)
    speed = Column(Float)
    engine_status = Column(Enum(EngineStatus))
    fuel_level = Column(Float)
    odometer = Column(Float)
    diagnostic_code = Column(StringList)
    timestamp = Column(DateTime, default=datetime.utcnow)

class Alert(Base):
    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True, index=True)
    vin = Column(String)
    type = Column(String)
    severity = Column(String)
    message = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)

class DiagnosticError(Base):
    __tablename__ = "digcodes"

    code = Column(String, primary_key=True, index=True)
    description = Column(String)
    severity = Column(String)
