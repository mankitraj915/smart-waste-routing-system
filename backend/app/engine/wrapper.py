import logging
import numpy as np
from datetime import datetime
from app.db.database import SessionLocal
from app.db.models import Bin, DailyRoute

import sys
import os
# Dynamically register the core engine path so algorithms can natively cross-reference each other cleanly without rewrite
sys.path.append(os.path.join(os.path.dirname(__file__), "core"))

from app.engine.core.prediction import predict_fill_levels, simulate_fill_levels, filter_active_nodes
from app.engine.core.distance import compute_distance_matrix
from app.engine.core.data import get_depot
from app.engine.core.hybrid import run_hybrid

logger = logging.getLogger(__name__)

def time_it_stub(func, *args, **kwargs):
    import time
    start = time.time()
    res = func(*args, **kwargs)
    return res, time.time() - start

def execute_daily_routing():
    db = SessionLocal()
    try:
        logger.info("Gathering active bins actively natively")
        bins = db.query(Bin).all()
        if not bins:
            coords = np.random.uniform(0, 100, size=(20, 2))
            for i, pt in enumerate(coords):
                db.add(Bin(lat=float(pt[0]), lng=float(pt[1])))
            db.commit()
            bins = db.query(Bin).all()
            
        num_nodes = len(bins)
        
        logger.info("Evaluating predictions seamlessly")
        historical_matrix = simulate_fill_levels(num_nodes=num_nodes, days_tracked=10)
        forecasted_volume = predict_fill_levels(historical_matrix)
        filtered_indices = filter_active_nodes(forecasted_volume, dispatch_threshold_percentage=60.0)
        
        active_bin_coords = np.array([[b.lat, b.lng] for b in bins])
        depot = get_depot()
        distance_matrix, all_pts = compute_distance_matrix(active_bin_coords, depot)
        
        operational_block = [0] + filtered_indices
        condensed_matrix = distance_matrix[np.ix_(operational_block, operational_block)]
        
        if len(filtered_indices) > 2:
            logger.info("Routing engine triggered purely analytically")
            from app.engine.core.aco import run_aco
            (filt_aco_route, aco_cost, aco_history) = run_aco(condensed_matrix, total_ants=10, max_iterations=50)[0:3]
            (filt_route, cost, _), _ = time_it_stub(run_hybrid, condensed_matrix, filt_aco_route, aco_history)
        else:
            filt_route = []
            
        today_str = datetime.utcnow().strftime("%Y-%m-%d")
        final_sequence = [int(operational_block[i]) for i in filt_route] if filt_route else []
        
        existing = db.query(DailyRoute).filter_by(truck_id="TRUCK-1", date=today_str).first()
        if existing:
            existing.route_sequence_json = final_sequence
        else:
            db.add(DailyRoute(truck_id="TRUCK-1", date=today_str, route_sequence_json=final_sequence))
            
        db.commit()
        logger.info("Saved structural bounds successfully perfectly")
        return final_sequence
    except Exception as e:
        db.rollback()
        logger.error(f"Fatal error natively bounded in matrix execution: {str(e)}")
        raise e
    finally:
        db.close()
