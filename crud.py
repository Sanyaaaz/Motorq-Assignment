from sqlalchemy.orm import Session
import models, schema
from datetime import datetime, timedelta

def create_vehicle(db: Session, vehicle: schema.VehicleCreate):
    db_vehicle = models.Vehicle(**vehicle.dict())
    db.add(db_vehicle)
    db.commit()
    db.refresh(db_vehicle)
    return db_vehicle

def get_vehicle(db: Session, vin: str):
    return db.query(models.Vehicle).filter(models.Vehicle.vin == vin).first()

def delete_vehicle(db: Session, vin: str):
    v = get_vehicle(db, vin)
    if v:
        db.delete(v)
        db.commit()
    return v

def get_vehicles(db: Session):
    return db.query(models.Vehicle).all()

def add_telemetry(db: Session, telemetry: schema.TelemetryCreate):
    data = models.Telemetry(**telemetry.dict())
    db.add(data)
    db.commit()
    db.refresh(data)
    return data

def get_telemetry_history(db: Session, vin: str):
    return db.query(models.Telemetry).filter(models.Telemetry.vin == vin).all()

def get_latest_telemetry(db: Session, vin: str):
    return db.query(models.Telemetry).filter(models.Telemetry.vin == vin).order_by(models.Telemetry.timestamp.desc()).first()

def get_active_inactive_counts(db: Session):
    cutoff = datetime.utcnow() - timedelta(hours=24)
    active = db.query(models.Telemetry.vin).filter(models.Telemetry.timestamp > cutoff).distinct().count()
    total = db.query(models.Vehicle).count()
    return {"active": active, "inactive": total - active}

def get_fuel_average(db: Session):
    from sqlalchemy import func
    return db.query(func.avg(models.Telemetry.fuel_level)).scalar()

def get_distance_last_24h(db: Session):
    cutoff = datetime.utcnow() - timedelta(hours=24)
    from sqlalchemy import func
    return db.query(func.sum(models.Telemetry.odometer)).filter(models.Telemetry.timestamp > cutoff).scalar() or 0