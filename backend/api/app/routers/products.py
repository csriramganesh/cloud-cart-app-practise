from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.api.app.database import get_db
from backend.api.app.models.product import Product


router = APIRouter(
    prefix="/api/v1/products",
    tags=["products"],
)


@router.get("")
def get_products(
    db: Session = Depends(get_db),
):
    return db.query(Product).all()
