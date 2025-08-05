from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import models, schema, crud, alerts
from database import SessionLocal, engine
from fastapi.middleware.cors import CORSMiddleware

models.Base.metadata.create_all(bind=engine)
app = FastAPI()

app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/vehicles", response_model=schema.Vehicle)
def create_vehicle(vehicle: schema.VehicleCreate, db: Session = Depends(get_db)):
    return crud.create_vehicle(db, vehicle)

@app.get("/vehicles", response_model=list[schema.Vehicle])
def list_vehicles(db: Session = Depends(get_db)):
    return crud.get_vehicles(db)

@app.get("/vehicles/{vin}", response_model=schema.Vehicle)
def get_vehicle(vin: str, db: Session = Depends(get_db)):
    v = crud.get_vehicle(db, vin)
    if not v:
        raise HTTPException(404)
    return v

@app.delete("/vehicles/{vin}")
def delete_vehicle(vin: str, db: Session = Depends(get_db)):
    return crud.delete_vehicle(db, vin)

@app.post("/telemetry", response_model=schema.Telemetry)
def receive_telemetry(data: schema.TelemetryCreate, db: Session = Depends(get_db)):
    t = crud.add_telemetry(db, data)
    alerts.check_alerts(db, t)
    return t

@app.get("/telemetry/{vin}", response_model=list[schema.Telemetry])
def history(vin: str, db: Session = Depends(get_db)):
    return crud.get_telemetry_history(db, vin)

@app.get("/telemetry/latest/{vin}", response_model=schema.Telemetry)
def latest(vin: str, db: Session = Depends(get_db)):
    return crud.get_latest_telemetry(db, vin)

@app.get("/alerts", response_model=list[schema.Alert])
def all_alerts(db: Session = Depends(get_db)):
    return db.query(models.Alert).all()

@app.get("/alerts/{id}", response_model=schema.Alert)
def get_alert(id: int, db: Session = Depends(get_db)):
    return db.query(models.Alert).filter(models.Alert.id == id).first()

@app.get("/analytics/summary")
def summary(db: Session = Depends(get_db)):
    return {
        "active_inactive": crud.get_active_inactive_counts(db),
        "avg_fuel_level": crud.get_fuel_average(db),
        "distance_last_24h": crud.get_distance_last_24h(db)
    }