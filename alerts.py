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
            message=f"Speed violation: {telemetry.speed} km/h",
            timestamp=datetime.now()
        ))


    if telemetry.fuel_level < 15:
        alerts.append(models.Alert(
            vin=telemetry.vin,
            type="LowFuel",
            severity="Medium",
            message=f"Low fuel level: {telemetry.fuel_level}%",
            timestamp=datetime.now()
        ))


    if telemetry.diagnostic_code:
        for code in telemetry.diagnostic_code:
            diagnostic = db.query(models.DiagnosticError).filter_by(code=code).first()
            if diagnostic:
                cnt = db.query(models.Alert).filter_by(vin=telemetry.vin).count()

               
                message = (
                    f"{code}: {diagnostic.description}"
                    if diagnostic.severity.lower() == "high" or cnt >= 10
                    else ""
                )

                alerts.append(models.Alert(
                    vin=telemetry.vin,
                    type="DiagnosticCode",
                    severity=diagnostic.severity,
                    message=message,
                    timestamp=datetime.now()
                ))


    for alert in alerts:
        db.add(alert)

    db.commit()
