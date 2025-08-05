from sqlalchemy import Column, String, Integer, Float, DateTime, Enum, ForeignKey
from sqlalchemy.orm import relationship
from database import Base
from sqlalchemy.types import TypeDecorator
import enum
import json
from datetime import datetime

class StatusEnum(str, enum.Enum):
    Active = "Active"
    Maintenance = "Maintainance"
    Decommissioned = "Decommissioned"

class EngineStatus(str, enum.Enum):
    On = "On"
    Off = "Off"
    Idle = "Idle"

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
    diagnostic_code = Column(String)
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
    __tablename__ = "dtc_codes"
    code = Column(String, primary_key=True, index=True)
    description = Column(String)
    severity = Column(String)