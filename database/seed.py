from backend.api.app.database import Base, SessionLocal, engine
from backend.api.app.models.product import Product


Base.metadata.create_all(
    bind=engine
)


db = SessionLocal()


try:
    existing = db.query(Product).count()

    if existing == 0:
        products = [
            Product(
                name="Mechanical Keyboard",
                price=4999,
            ),
            Product(
                name="Wireless Mouse",
                price=1999,
            ),
            Product(
                name="USB-C Dock",
                price=3499,
            ),
            Product(
                name="DevOps Hoodie",
                price=1499,
            ),
        ]

        db.add_all(products)
        db.commit()

        print(
            "CloudCart products seeded."
        )

    else:
        print(
            "Products already exist."
        )

finally:
    db.close()
