from sqlalchemy.orm import Session
import models, schema

def addtele(db: Session, telemetry: schema.TelemetryCreate):
    entry = models.Telemetry(**telemetry.dict())
    db.add(entry)
    db.commit()
    db.refresh(entry)
    return entry

def gettelemetryhistory(db: Session, vin: str):
    return db.query(models.Telemetry).filter(models.Telemetry.vin == vin).all()

def getlatesttelemetry(db: Session, vin: str):
    return db.query(models.Telemetry).filter(models.Telemetry.vin == vin).order_by(models.Telemetry.timestamp.desc()).first()
