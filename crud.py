from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import models, schema



def create_vehicle(db: Session, vehicle: schema.VehicleCreate):
    new_vehicle = models.Vehicle(**vehicle.dict())
    db.add(new_vehicle)
    db.commit()
    db.refresh(new_vehicle)
    return new_vehicle

def get_vehicle(db: Session, vin: str):
    return db.query(models.Vehicle).filter(models.Vehicle.vin == vin).first()

def delete_vehicle(db: Session, vin: str):
    vehicle = get_vehicle(db, vin)
    if vehicle:
        db.delete(vehicle)
        db.commit()
    return vehicle

def get_vehicles(db: Session):
    return db.query(models.Vehicle).all()



def add_telemetry(db: Session, telemetry: schema.TelemetryCreate):
    record = models.Telemetry(**telemetry.dict())
    db.add(record)
    db.commit()
    db.refresh(record)
    return record

def get_telemetry_history(db: Session, vin: str):
    return db.query(models.Telemetry).filter(models.Telemetry.vin == vin).all()

def get_latest_telemetry(db: Session, vin: str):
    return db.query(models.Telemetry)\
        .filter(models.Telemetry.vin == vin)\
        .order_by(models.Telemetry.timestamp.desc())\
        .first()



def get_active_inactive_counts(db: Session):
    result = {}
    cutoff_time = datetime.now() - timedelta(hours=24)

    vehicles = db.query(models.Vehicle).all()
    for vehicle in vehicles:
        latest_data = db.query(models.Telemetry)\
                        .filter(models.Telemetry.vin == vehicle.vin)\
                        .order_by(models.Telemetry.timestamp.desc())\
                        .first()
        if latest_data and latest_data.timestamp > cutoff_time:
            result[vehicle.vin] = "active"
        else:
            result[vehicle.vin] = "inactive"
    return result

def get_fuel_average(db: Session):
    result = {}

    vehicles = db.query(models.Vehicle).all()
    for vehicle in vehicles:
        entries = db.query(models.Telemetry)\
                    .filter(models.Telemetry.vin == vehicle.vin)\
                    .all()
        total = 0
        count = 0
        for record in entries:
            if record.fuel_level is not None:
                total += record.fuel_level
                count += 1
        if count > 0:
            result[vehicle.vin] = round(total / count, 2)
        else:
            result[vehicle.vin] = None
    return result

def get_distance_last_24h(db: Session):
    result = {}
    cutoff_time = datetime.now() - timedelta(hours=24)

    vehicles = db.query(models.Vehicle).all()
    for vehicle in vehicles:
        records = db.query(models.Telemetry)\
                    .filter(models.Telemetry.vin == vehicle.vin,
                            models.Telemetry.timestamp > cutoff_time)\
                    .order_by(models.Telemetry.timestamp)\
                    .all()
        if len(records) >= 2:
            start = records[0].odometer
            end = records[-1].odometer
            distance = end - start
        else:
            distance = 0
        result[vehicle.vin] = round(distance, 2)
    return result
