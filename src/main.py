import sys
from tkinter import messagebox

from src.db.config_load import load_config, ConfigError

from src.db.database import Database
from src.db.dao.rental import Rental
from src.db.dao.rv import Rv
from src.db.dao.customer import Customer
from src.db.dao.brand import Brand
from src.db.dao.rv_type import RvType
from src.db.dao.accessory import Accessory
from src.db.dao.accessory_rental import AccessoryRental
from src.db.report import Report

from app.services.rental_service import RentalService
from app.services.rv_service import RvService
from app.services.customer_service import CustomerService
from app.services.brand_service import BrandService
from app.services.rv_type_service import RvTypeService
from app.services.accessory_service import AccessoryService
from app.services.report_service import ReportService
from app.services.import_service import ImportService

from src.ui.main_window import create_application


def initialize_application():
    try:
        print("Loading configuration...")
        config = load_config("db/config.json")

        print("Connecting to database...")
        db = Database(config)

        rental_dao = Rental(db)
        rv_dao = Rv(db)
        customer_dao = Customer(db)
        brand_dao = Brand(db)
        rv_type_dao = RvType(db)
        accessory_dao = Accessory(db)
        accessory_rental_dao = AccessoryRental(db)
        report = Report(db)

        print("Database layer initialized")

        print("Initializing services...")

        rental_service = RentalService(
            rental_dao=rental_dao,
            rv_dao=rv_dao,
            customer_dao=customer_dao,
            accessory_dao=accessory_dao
        )

        rv_service = RvService(
            rv_dao=rv_dao,
            brand_dao=brand_dao,
            rv_type_dao=rv_type_dao
        )

        customer_service = CustomerService(customer_dao=customer_dao)

        brand_service = BrandService(brand_dao=brand_dao,rv_dao=rv_dao)

        rv_type_service = RvTypeService(rv_type_dao=rv_type_dao,rv_dao=rv_dao)

        accessory_service = AccessoryService(accessory_dao=accessory_dao)

        report_service = ReportService(report=report)

        import_service = ImportService(
            customer_dao=customer_dao,
            brand_dao=brand_dao,
            rv_type_dao=rv_type_dao,
            accessory_dao=accessory_dao
        )

        print("Application layer initialized")

        services = {
            'rental': rental_service,
            'rv': rv_service,
            'customer': customer_service,
            'brand': brand_service,
            'rv_type': rv_type_service,
            'accessory': accessory_service,
            'report': report_service,
            'import': import_service,
            'database': db
        }

        return services

    except ConfigError as e:
        messagebox.showerror(
            "Configuration Error",
            f"Error loading configuration:\n{str(e)}\n\n"
            f"Please check db/config.json file."
        )
        return None

    except Exception as e:
        messagebox.showerror(
            "Initialization Error",
            f"Error initializing application:\n{str(e)}\n\n"
            f"Please check database connection and configuration."
        )
        import traceback
        traceback.print_exc()
        return None


def main():
    print("=" * 50)
    print("RV Rental Management System")
    print("=" * 50)

    services = initialize_application()

    if services is None:
        print("Application initialization failed")
        sys.exit(1)

    print("All layers initialized successfully")
    print("=" * 50)

    try:
        print("Starting user interface...")
        app = create_application(services)

        app.run()

    except Exception as e:
        messagebox.showerror("Application Error", f"Unexpected error: {str(e)}")
        import traceback
        traceback.print_exc()

    finally:
        print("\nClosing database connection...")
        if 'database' in services:
            services['database'].close()
        print("Database connection closed")
        print("Application terminated")


if __name__ == "__main__":
    main()