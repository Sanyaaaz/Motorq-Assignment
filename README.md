

# Motorq Assignment

This is a FastAPI-based backend system for managing and monitoring a fleet of connected vehicles. The system supports telemetry tracking, alert generation, and basic analytics for fleet insights.

## Features

### Vehicle Management

* Add new vehicles
* List all vehicles
* Retrieve vehicle by VIN
* Delete a vehicle

### Telemetry Tracking

* Submit telemetry data (location, speed, fuel level, engine status, diagnostic codes)
* Retrieve latest telemetry per vehicle
* View full telemetry history

### Alerts

* Alerts generated for:

  * Speed violations (over 100 km/h)
  * Low fuel level (below 15%)
  * Diagnostic trouble codes (with messages shown only if severity is high or if total alerts for a vehicle ≥ 10)
* View all alerts
* View alert by ID

### Analytics

* Count of active vs inactive vehicles (based on telemetry in the last 24 hours)
* Average fuel level per vehicle
* Total distance traveled by each vehicle in the last 24 hours

## Setup Instructions

### Prerequisites

* Python 3.9 or higher
* pip (Python package installer)
* Virtual environment (optional but recommended)

### Installation

1. Clone the repository:

```bash
git clone https://github.com/your-username/connected-car-fleet.git
cd connected-car-fleet
```

2. Set up and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate      # macOS/Linux
venv\Scripts\activate         # Windows
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Run the FastAPI server:

```bash
uvicorn main:app --reload
```

5. Open your browser and navigate to:

```
http://127.0.0.1:8000/docs
```

This opens the interactive Swagger UI.

## File Structure

```
.
├── main.py               # FastAPI application entrypoint
├── models.py             # SQLAlchemy models
├── schema.py             # Pydantic schemas
├── database.py           # Database configuration
├── dummydata.py          # Diagnostic code seeding
├── alerts.py             # Alert logic
├── crud/
│   ├── __init__.py
│   ├── vehicle.py        # CRUD operations for vehicles
│   ├── telemetry.py      # CRUD operations for telemetry
│   └── analytics.py      # Fleet analytics functions
└── fleet.db              # SQLite database (auto-created)
```

