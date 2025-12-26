class CustomerServiceException(Exception):
    pass

class CustomerService:
    def __init__(self, customer_dao):
        self.customer_dao = customer_dao

    def create_customer(self, name, surname, email, tel):

        if not name or not name.strip():
            raise CustomerServiceException("Name cannot be empty")

        if not surname or not surname.strip():
            raise CustomerServiceException("Surname cannot be empty")

        if '@' not in email or '.' not in email:
            raise CustomerServiceException("Invalid email format")

        if len(tel) < 9:
            raise CustomerServiceException("Phone number must be at least 9 digits")

        self.customer_dao.create_customer(name.strip(), surname.strip(), email.strip(), tel.strip())

    def get_all_customers(self):

        return self.customer_dao.all_customers()

    def get_all_cutomers_with_ids(self):

        return self.customer_dao.all_customers_with_ids()

    def get_customer_by_id(self, customer_id):

        return self.customer_dao.select_customer_by_id(customer_id)

    def update_customer(self, customer_id, name=None, surname=None, email=None, tel=None):

        if email is not None and ('@' not in email or '.' not in email):
            raise CustomerServiceException("Invalid email format")

        if tel is not None and len(tel) < 9:
            raise CustomerServiceException("Phone number must be at least 9 digits")

        self.customer_dao.update_customer(customer_id, name, surname, email, tel)

    def delete_customer(self, customer_id):

        self.customer_dao.delete_customer(customer_id)

    def search_customer_by_email(self, email):

        return self.customer_dao.search_by_email(email)





