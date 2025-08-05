from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from database import SessionLocal, engine
import models
from dummydata import populate_dtc_codes
from crud import vehicle, telemetry, analytics
import alerts
import schema

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/vehicles", response_model=schema.Vehicle)
def add_vehicle(vehicle_data: schema.VehicleCreate, db: Session = Depends(get_db)):
    return vehicle.create_vehicle(db, vehicle_data)

@app.get("/vehicles", response_model=list[schema.Vehicle])
def get_all_vehicles(db: Session = Depends(get_db)):
    return vehicle.get_vehicles(db)

@app.get("/vehicles/{vin}", response_model=schema.Vehicle)
def get_vehicle_by_vin(vin: str, db: Session = Depends(get_db)):
    result = vehicle.get_vehicle(db, vin)
    if not result:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    return result

@app.delete("/vehicles/{vin}")
def remove_vehicle(vin: str, db: Session = Depends(get_db)):
    result = vehicle.delete_vehicle(db, vin)
    if not result:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    return {"message": f"{vin} removed"}


@app.post("/telemetry", response_model=schema.Telemetry)
def submit_telemetry(data: schema.TelemetryCreate, db: Session = Depends(get_db)):
    record = telemetry.addtele(db, data)
    alerts.check_alerts(db, record)
    return record

@app.get("/telemetry/{vin}", response_model=list[schema.Telemetry])
def telemetry_history(vin: str, db: Session = Depends(get_db)):
    return telemetry.get_telemetry_history(db, vin)

@app.get("/telemetry/latest/{vin}", response_model=schema.Telemetry)
def latest_telemetry(vin: str, db: Session = Depends(get_db)):
    latest = telemetry.get_latest_telemetry(db, vin)
    if not latest:
        raise HTTPException(status_code=404, detail="No telemetry found")
    return latest

@app.get("/analytics/summary")
def summary(db: Session = Depends(get_db)):
    return {
        "active_inactive": analytics.getcount(db),
        "avg_fuel": analytics.fuelavg(db),
        "distance_last_24h": analytics.dist(db)
    }

@app.get("/analytics/{vin}")
def analytics_by_vehicle(vin: str, db: Session = Depends(get_db)):
    active_status = analytics.getcount(db)
    fuel_avg = analytics.fuelavg(db)
    distance = analytics.dist(db)

    return {
        "vin": vin,
        "active_status": active_status.get(vin),
        "avg_fuel": fuel_avg.get(vin),
        "distance_last_24h": distance.get(vin)
    }
@app.get("/alerts", response_model=list[schema.Alert])
def alerts_all(db: Session = Depends(get_db)):
    return db.query(models.Alert).all()



@app.on_event("startup")
def startup_init():
    db = SessionLocal()
    try:
        populate_dtc_codes(db)
    finally:
        db.close()
