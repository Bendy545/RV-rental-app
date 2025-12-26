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
        rentals = self.rental_dao.all_rentals()

        formatted = []
        for rental in rentals:
            formatted.append({
                'date_from': rental[0],
                'date_to': rental[1],
                'creation_date': rental[2],
                'price': float(rental[3]),
                'status': rental[4],
                'is_paid': 'Yes' if rental[5] == 1 else 'No',
                'customer_email': rental[6],
                'rv_spz': rental[7]
            })

        return formatted

    def get_all_rentals_with_ids(self):
        rentals = self.rental_dao.all_rentals_with_ids()

        formatted = []
        for rental in rentals:
            formatted.append({
                'id': rental[0],  # Rental ID
                'date_from': rental[1],
                'date_to': rental[2],
                'creation_date': rental[3],
                'price': float(rental[4]),
                'status': rental[5],
                'is_paid': 'Yes' if rental[6] == 1 else 'No',
                'customer_email': rental[7],
                'rv_spz': rental[8]
            })

        return formatted

    def update_rental_status(self, rental_id, new_status):

        valid_statuses = ['reserved', 'active', 'finished', 'canceled']
        if new_status not in valid_statuses:
            raise ValueError(f"Invalid status. Must be one of: {valid_statuses}")

        self.rental_dao.update_rental(rental_id, status=new_status)

    def mark_rental_as_paid(self, rental_id):

        self.rental_dao.update_rental(rental_id, is_paid=1)

    def cancel_rental(self, rental_id):

        self.rental_dao.update_rental(rental_id, status='canceled')

    def delete_rental(self, rental_id):

        self.rental_dao.delete_rental(rental_id)

    def get_rental_details(self, rental_id):

        return self.rental_dao.get_rental_with_accessories(rental_id)