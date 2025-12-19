import sys
from datetime import date

from db.config_load import load_config
from db.database import Database
from src.db.dao.accessory import Accessory
from src.db.dao.accessory_rental import AccessoryRental
from src.db.dao.brand import Brand
from src.db.dao.customer import Customer
from src.db.dao.rental import Rental
from src.db.dao.rv import Rv
from src.db.dao.rv_type import RvType



def main():
    config = load_config("db/config.json")
    db = Database(config)

    accessory = Accessory(db)
    accessory_rental = AccessoryRental(db)
    brand = Brand(db)
    customer = Customer(db)
    rental = Rental(db)
    rv = Rv(db)
    rv_type = RvType(db)

    rental.create_rental(
        date_from=date(2024, 12, 20),
        date_to=date(2024, 12, 25),
        creation_date=date.today(),
        price=500.00,
        id_customer=1,
        id_rv=1
    )
    # Output: "Rental created successfully (no accessories)"

    # ========================================
    # Example 2: Rental WITH ONE accessory
    # ========================================
    accessories = [
        {'id_accessory': 2, 'amount': 1, 'price': 50.0}
    ]

    rental_id = rental.create_rental(
        date_from=date(2024, 12, 26),
        date_to=date(2024, 12, 30),
        creation_date=date.today(),
        price=700.00,
        id_customer=2,
        id_rv=1,
        accessories_list=accessories
    )

    accessories = [
        {'id_accessory': 1, 'amount': 2, 'price': 30.0},
        {'id_accessory': 3, 'amount': 1, 'price': 100.0},
        {'id_accessory': 2, 'amount': 4, 'price': 15.0}
    ]

    rental_id = rental.create_rental(
        date_from=date(2025, 1, 5),
        date_to=date(2025, 1, 12),
        creation_date=date.today(),
        price=1200.00,
        id_customer=1,
        id_rv=2,
        accessories_list=accessories
    )

    print(f"Created rental with ID: {rental_id}")

    """brand.create_brand("Volkswagen")
    brand.create_brand("Fiat")
    brand.create_brand("Mercedes")

    rv_type.create_type("Van", "Compact camper")
    rv_type.create_type("Alcove", "Family camper")
    rv_type.create_type("Integrovan", "Luxury camper")

    rv.create_rv(
        spz="1AB2345",
        manufacture_date=date(2019, 5, 10),
        price_for_day=2500,
        status="available",
        id_brand=1,
        id_type=1
    )

    rv.create_rv(
        spz="2BC3456",
        manufacture_date=date(2020, 6, 15),
        price_for_day=3200,
        status="rented",
        id_brand=2,
        id_type=2
    )

    customer.create_customer(
        name="Jan",
        surname="Novak",
        email="jan.novak@email.cz",
        tel="777111222"
    )

    customer.create_customer(
        name="Petra",
        surname="Svobodova",
        email="petra.s@email.cz",
        tel="777333444"
    )

    rental.create_rental(
        date_from=date(2024, 7, 1),
        date_to=date(2024, 7, 7),
        creation_date=date(2024, 6, 15),
        price=18000,
        status="finished",
        is_paid=1,
        id_customer=1,
        id_rv=1
    )

    rental.create_rental(
        date_from=date(2024, 8, 10),
        date_to=date(2024, 8, 15),
        creation_date=date(2024, 7, 20),
        price=15000,
        status="active",
        is_paid=0,
        id_customer=2,
        id_rv=2
    )

    accessory.create_accessory("Nosic kol", "Nosic kol pro 2 kola", 150.00)
    accessory.create_accessory("Kempingovy stul", "Skladaci stul", 50.00)
    accessory.create_accessory("Gril", "Plynovy gril", 120.00)


    accessory_rental.create_accessory_rental(
        id_accessory=1,
        id_rental=1,
        amount=1,
        price_at_rent=150
    )

    accessory_rental.create_accessory_rental(
        id_accessory=2,
        id_rental=1,
        amount=1,
        price_at_rent=50
    )

    accessory_rental.create_accessory_rental(
        id_accessory=3,
        id_rental=2,
        amount=1,
        price_at_rent=120
    )
    """



if __name__ == "__main__":
    main()