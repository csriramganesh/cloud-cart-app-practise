from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.api.app.database import get_db
from backend.api.app.models.order import Order
from backend.api.app.models.product import Product
from backend.api.app.schemas.order import OrderCreate
from backend.worker.tasks import process_order


router = APIRouter(
    prefix="/api/v1/orders",
    tags=["orders"],
)


@router.get("")
def get_orders(
    db: Session = Depends(get_db),
):
    return db.query(Order).all()


@router.get("/{order_id}")
def get_order(
    order_id: int,
    db: Session = Depends(get_db),
):
    order = (
        db.query(Order)
        .filter(Order.id == order_id)
        .first()
    )

    if order is None:
        raise HTTPException(
            status_code=404,
            detail="Order not found",
        )

    return order


@router.post("")
def create_order(
    payload: OrderCreate,
    db: Session = Depends(get_db),
):
    product = (
        db.query(Product)
        .filter(Product.id == payload.product_id)
        .first()
    )

    if product is None:
        raise HTTPException(
            status_code=404,
            detail="Product not found",
        )

    order = Order(
        product_id=product.id,
        quantity=payload.quantity,
        total_price=product.price * payload.quantity,
        status="PENDING",
    )

    db.add(order)
    db.commit()
    db.refresh(order)

    process_order.delay(order.id)

    return {
        "message": "Order created",
        "order": order,
    }
