import logging
import redis
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from app.db.database import get_db
from app.db.models import Telemetry, DailyRoute
from app.api.schemas import TelemetryCreate, CalculateResponse, DailyRouteResponse
from app.celery_worker.tasks import run_daily_optimization

# Setup logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

router = APIRouter()
redis_client = redis.Redis(host='redis', port=6379, db=0)

@router.post("/telemetry", response_model=dict)
def log_telemetry(payload: TelemetryCreate, db: Session = Depends(get_db)):
    try:
        db_telemetry = Telemetry(
            bin_id=payload.bin_id,
            fill_percentage=payload.fill_percentage,
            timestamp=datetime.utcnow()
        )
        db.add(db_telemetry)
        db.commit()
        logger.info(f"Recorded telemetry for bin {payload.bin_id}")
        return {"status": "recorded"}
    except Exception as e:
        db.rollback()
        logger.error(f"Failed to record telemetry: {str(e)}")
        raise HTTPException(status_code=500, detail="Database write failed")

@router.post("/routes/calculate", response_model=CalculateResponse)
def calculate_routes():
    # Distributed idempotency lock
    lock_acquired = redis_client.set("route_calculation_lock", "locked", nx=True, ex=300)
    if not lock_acquired:
        logger.warning("Duplicate route calculation triggered. Rejecting.")
        raise HTTPException(status_code=409, detail="Computation already running")
        
    try:
        task = run_daily_optimization.delay()
        logger.info(f"Dispatched optimization task {task.id}")
        return {"task_id": str(task.id), "status": "processing"}
    except Exception as e:
        redis_client.delete("route_calculation_lock")
        logger.error(f"Failed to enqueue task: {str(e)}")
        raise HTTPException(status_code=500, detail="Queue unreachable")

@router.get("/routes/{truck_id}", response_model=DailyRouteResponse)
def get_routes(truck_id: str, date: str, db: Session = Depends(get_db)):
    try:
        route = db.query(DailyRoute).filter(DailyRoute.truck_id == truck_id, DailyRoute.date == date).first()
        if not route:
            raise HTTPException(status_code=404, detail="Route not found")
        return {"truck_id": route.truck_id, "date": route.date, "route_sequence_json": route.route_sequence_json}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Database read failed: {str(e)}")
        raise HTTPException(status_code=500, detail="Read operation failed")
