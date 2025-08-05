This repository contains a FastAPI-based backend for managing and monitoring a fleet of connected vehicles. The system handles telemetry data, diagnostics, and alert generation, and provides useful analytics on vehicle activity and status.

Overview
The system supports:

Vehicle CRUD operations

Telemetry data ingestion and storage

Alert generation based on rules and diagnostics

Per-vehicle and fleet-wide analytics

Auto-initialization of diagnostic codes

Swagger documentation for testing and reference

Features
Vehicle Management:

Add, view, retrieve, and delete vehicles from the fleet

Telemetry Tracking:

Submit real-time telemetry data (speed, location, fuel level, engine status, diagnostics)

Automatically triggers alerts if predefined rules are violated

Alerts:

Alerts generated for speed, fuel level, and diagnostic codes

Alerts are stored and retrievable via endpoints

Diagnostic messages are shown only if severity is high or alert count exceeds 10 for a VIN

Analytics:

Active vs Inactive vehicles (based on last telemetry within 24 hours)

Average fuel level per vehicle

Distance traveled in the last 24 hours

Getting Started
Prerequisites
Python 3.9 or above

pip

(Optional) Virtual Environment

Installation
Clone the repository:

bash
Copy
Edit
git clone https://github.com/your-username/connected-car-fleet.git
cd connected-car-fleet
Create a virtual environment and activate it:

bash
Copy
Edit
python -m venv venv
source venv/bin/activate   -Linus/mac
venv\Scripts\activate      -Windows
Install dependencies:

bash
Copy
Edit
pip install -r requirements.txt
Run the FastAPI server:

bash
Copy
Edit
uvicorn main:app --reload
Open the Swagger UI to explore endpoints:

http://127.0.0.1:8000/docs

API Endpoints
Vehicles
POST /vehicles → Add a new vehicle

GET /vehicles → Get all vehicles

GET /vehicles/{vin} → Get a vehicle by VIN

DELETE /vehicles/{vin} → Delete a vehicle

Telemetry
POST /telemetry → Submit telemetry data

GET /telemetry/{vin} → Get all telemetry records for a vehicle

GET /telemetry/latest/{vin} → Get latest telemetry for a vehicle

Alerts
GET /alerts → List all alerts

GET /alerts/{id} → Get alert details by ID

Analytics
GET /analytics/summary → Get summary analytics (active/inactive, fuel avg, distance)

GET /analytics/{vin} → Get per-vehicle analytics

Diagnostic Codes
On application startup, diagnostic codes are auto-populated into the digcodes table. These are used to evaluate incoming telemetry for issues.

Alert Logic
Speed over 100 triggers a speed alert

Fuel level below 15 triggers a low fuel alert

Diagnostic code alerts depend on severity (only high or when vehicle has 10+ alerts)

Folder Structure
main.py — FastAPI application and routing

database.py — Database connection setup

models.py — SQLAlchemy ORM models

schema.py — Pydantic models

dummydata.py — Seeds initial diagnostic code data

crud/

vehicle.py — Vehicle operations

telemetry.py — Telemetry operations

analytics.py — Fleet analytics

alerts.py — Alert generation logic


Swagger UI available at /docs

Designed for extensibility and easy deployment
