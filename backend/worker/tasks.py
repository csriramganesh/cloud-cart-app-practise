import time

from backend.api.app.database import SessionLocal
from backend.api.app.models.order import Order
from backend.worker.celery_app import celery_app


@celery_app.task(name="process_order")
def process_order(order_id: int):
    db = SessionLocal()

    try:
        order = (
            db.query(Order)
            .filter(Order.id == order_id)
            .first()
        )

        if order is None:
            return {
                "order_id": order_id,
                "status": "not_found",
            }

        order.status = "PROCESSING"
        db.commit()

        print(f"Processing order {order_id}...")

        time.sleep(5)

        order.status = "COMPLETED"
        db.commit()

        print(
            f"Order {order_id} processed successfully."
        )

        return {
            "order_id": order_id,
            "status": "COMPLETED",
        }

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()
