from datetime import datetime, date
from decimal import Decimal
import csv
import json

class RentalServiceException(Exception):
    pass

class RentalService:
    def __init__(self, rental_dao, rv_dao, customer_dao, accessory_dao):
        self.rental_dao = rental_dao
        self.rv_dao = rv_dao
        self.customer_dao = customer_dao
        self.accessory_dao = accessory_dao

    def create_new_rental(self, date_from, date_to, id_customer, id_rv, accessories_list=None):
        if date_from >= date_to:
            raise RentalServiceException("Date from must be before date to")

        if not self.customer_dao.select_customer_by_id(id_customer):
            raise RentalServiceException(f"Customer with ID {id_customer} does not exist")

        rv = self.rv_dao.select_rv_by_id(id_rv)
        if not rv:
            raise RentalServiceException(f"RV with ID {id_rv} does not exist")

        days = (date_to - date_from).days
        rv_price_per_day = rv[2]
        total_price = Decimal(rv_price_per_day) * days

        accessories_with_price = []
        if accessories_list:
            for acc in accessories_list:
                accessory = self.accessory_dao.select_accessory_by_id(acc['id_accessory'])
                if not accessory:
                    raise ValueError(f"Accessory with ID {acc['id_accessory']} does not exist")

                acc_price = Decimal(accessory[2]) * days * acc['amount']
                total_price += acc_price

                accessories_with_price.append({
                    'id_accessory': acc['id_accessory'],
                    'amount': acc['amount'],
                    'price': acc_price
                })

        creation_date = date.today()
        rental_id = self.rental_dao.create_rental(
            date_from=date_from,
            date_to=date_to,
            creation_date=creation_date,
            price=total_price,
            id_customer=id_customer,
            id_rv=id_rv,
            accessories_list=accessories_with_price if accessories_with_price else None
        )

        return rental_id

    def get_all_rentals_formatted(self):
        raise NotImplemented

    def mark_rental_as_paid(self, rental_id):
        raise NotImplemented

    def cancel_rental(self, rental_id):
        raise NotImplemented

    def delete_rental(self, rental_id):
        raise NotImplemented

    def get_rental_details(self):
        raise NotImplemented