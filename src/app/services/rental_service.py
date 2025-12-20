class RentalService:
    def __init__(self, db_connection, rental_dao, rv_dao, customer_dao, accessory_dao, accessory_rental_dao):
        self.db_connection = db_connection
        self.rental_dao = rental_dao
        self.rv_dao = rv_dao
        self.customer_dao = customer_dao
        self.accessory_dao = accessory_dao
        self.accessory_rental_dao = accessory_rental_dao