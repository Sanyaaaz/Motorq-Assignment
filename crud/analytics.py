from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import models

def getcount(db: Session):
    cutoff = datetime.now() - timedelta(hours=24)
    result = {}

    vehicles = db.query(models.Vehicle).all()
    for vehicle in vehicles:
        latest = db.query(models.Telemetry)\
                   .filter(models.Telemetry.vin == vehicle.vin)\
                   .order_by(models.Telemetry.timestamp.desc()).first()
        if latest and latest.timestamp > cutoff:
            result[vehicle.vin] = "active"
        else:
            result[vehicle.vin] = "inactive"
    return result

def fuelavg(db: Session):
    result = {}
    for v in db.query(models.Vehicle).all():
        telemetries = db.query(models.Telemetry).filter(models.Telemetry.vin == v.vin).all()
        values = [t.fuel_level for t in telemetries if t.fuel_level is not None]
        if values:
            result[v.vin] = round(sum(values) / len(values), 2)
        else:
            result[v.vin] = None
    return result

def dist(db: Session):
    cutoff = datetime.now() - timedelta(hours=24)
    result = {}

    for v in db.query(models.Vehicle).all():
        records = db.query(models.Telemetry).filter(
            models.Telemetry.vin == v.vin,
            models.Telemetry.timestamp > cutoff
        ).order_by(models.Telemetry.timestamp).all()

        if len(records) >= 2:
            distance = records[-1].odometer - records[0].odometer
        else:
            distance = 0
        result[v.vin] = round(distance, 2)
    return result
