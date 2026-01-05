from src.db.dao.customer import CustomerDAOException, CustomerNotFoundError as DAONotFound, CustomerDatabaseError as DAODatabase

class CustomerServiceException(Exception):
    pass
class CustomerValidationError(CustomerServiceException):
    pass
class CustomerNotFoundError(CustomerServiceException):
    pass
class CustomerDatabaseError(CustomerServiceException):
    pass

class CustomerService:
    def __init__(self, customer_dao):
        self.customer_dao = customer_dao

    def _validate_data(self, name, surname, email, tel):
        if not name or not name.strip():
            raise CustomerValidationError("Name cannot be empty")
        if not surname or not surname.strip():
            raise CustomerValidationError("Surname cannot be empty")
        self._validate_email(email)
        if not tel or len(tel.strip()) < 9:
            raise CustomerValidationError("Phone number must be at least 9 digits")

    def _validate_email(self, email):
        if not email or '@' not in email or '.' not in email:
            raise CustomerValidationError("Invalid email format")

    def create_customer(self, name, surname, email, tel):
        try:
            self._validate_data(name, surname, email, tel)
            self.customer_dao.create_customer(name.strip(), surname.strip(), email.strip(), tel.strip())
        except CustomerValidationError:
            raise
        except DAODatabase as e:
            raise CustomerDatabaseError(str(e)) from e
        except CustomerDAOException as e:
            raise CustomerServiceException(f"Unexpected error: {str(e)}")

    def get_all_customers(self):

        return self.customer_dao.all_customers()

    def get_all_customers_with_ids(self):

        return self.customer_dao.all_customers_with_ids()

    def get_customer_by_id(self, customer_id):
        customer = self.customer_dao.select_customer_by_id(customer_id)
        if not customer:
            raise CustomerNotFoundError(f"Customer {customer_id} not found")
        return customer

    def update_customer(self, customer_id, name=None, surname=None, email=None, tel=None):

        try:
            if email is not None:
                self._validate_email(email)
            if tel is not None and len(tel) < 9:
                raise CustomerValidationError("Phone number must be at least 9 digits")

            self.customer_dao.update_customer(customer_id, name, surname, email, tel)

        except DAONotFound:
            raise CustomerNotFoundError(f"Customer with ID {customer_id} not found")
        except DAODatabase as e:
            raise CustomerDatabaseError(str(e)) from e
        except CustomerDAOException as e:
            raise CustomerServiceException(str(e))

    def delete_customer(self, customer_id):
        try:
            self.customer_dao.delete_customer(customer_id)
        except DAONotFound:
            raise CustomerNotFoundError(f"Customer with ID {customer_id} not found")
        except DAODatabase as e:
            raise CustomerDatabaseError(f"Cannot delete customer: {str(e)}")
        except CustomerDAOException as e:
            raise CustomerServiceException(str(e))

    def search_customer_by_email(self, email):

        return self.customer_dao.search_by_email(email)





