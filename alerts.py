from sqlalchemy.orm import Session
from datetime import datetime
import models

def check_alerts(db: Session, telemetry: models.Telemetry):
    alerts = []

    if telemetry.speed > 100:
        alerts.append(models.Alert(
            vin=telemetry.vin,
            type="Speed",
            severity="High",
            message=f"Speed violation: {telemetry.speed} km/h"
        ))

    if telemetry.fuel_level < 15:
        alerts.append(models.Alert(
            vin=telemetry.vin,
            type="LowFuel",
            severity="Medium",
            message=f"Low fuel level: {telemetry.fuel_level}%"
        ))

    for alert in alerts:
        alert.timestamp = datetime.utcnow()
        db.add(alert)

    db.commit()