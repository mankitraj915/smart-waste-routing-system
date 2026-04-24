from pydantic import BaseModel
from typing import List, Dict, Any

class TelemetryCreate(BaseModel):
    bin_id: int
    fill_percentage: float

class CalculateResponse(BaseModel):
    task_id: str
    status: str

class DailyRouteResponse(BaseModel):
    truck_id: str
    date: str
    route_sequence_json: List[int]
