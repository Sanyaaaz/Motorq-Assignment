from sqlalchemy.orm import Session
from database import SessionLocal, engine
import models
from datetime import datetime

def populate_dtc_codes(db: Session):
    codes = [
        {"code": "P0420", "description": "Efficiency below threshold", "severity": "High"},
        {"code": "P0302", "description": "Spark detected", "severity": "Medium"},
        {"code": "P0171", "description": "System not responding", "severity": "Medium"},
    ]
    for c in codes:
        if not db.query(models.DiagnosticError).filter_by(code=c["code"]).first():
            db.add(models.DiagnosticError(**c))
    db.commit()

