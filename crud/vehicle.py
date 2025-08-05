from sqlalchemy.orm import Session
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
    v = get_vehicle(db, vin)
    if v:
        db.delete(v)
        db.commit()
    return v

def get_vehicles(db: Session):
    return db.query(models.Vehicle).all()
