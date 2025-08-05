from sqlalchemy.orm import Session
import models
from collections import defaultdict

def alert(db: Session):
    result = defaultdict(int)
    alerts = db.query(models.Alert).all()
    for alert in alerts:
        key = (alert.type, alert.severity)
        result[key] += 1
    return dict(result)
