import logging
import redis
from app.celery_worker.celery_app import celery_app
from app.engine.wrapper import execute_daily_routing

logger = logging.getLogger(__name__)
redis_client = redis.Redis(host='redis', port=6379, db=0)

@celery_app.task(bind=True, max_retries=3)
def run_daily_optimization(self):
    try:
        logger.info("Initializing background routing pipeline...")
        sequence = execute_daily_routing()
        logger.info("Pipeline successful natively")
        return sequence
    except Exception as e:
        logger.error(f"Routing Pipeline Crash: {str(e)}")
        try:
            self.retry(countdown=60)
        except self.MaxRetriesExceededError:
            logger.error("Maximum retries exhausted natively. System failed explicitly.")
            raise e
    finally:
        # Strict mechanism clearing distributed limits ensuring next runs pass
        redis_client.delete("route_calculation_lock")
