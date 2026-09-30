from sqlalchemy import Column, Float, Integer, String

from backend.api.app.database import Base


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)

    product_id = Column(
        Integer,
        nullable=False,
    )

    quantity = Column(
        Integer,
        nullable=False,
    )

    total_price = Column(
        Float,
        nullable=False,
    )

    status = Column(
        String(50),
        nullable=False,
        default="PENDING",
    )
