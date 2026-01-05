import cx_Oracle

class CustomerDAOException(Exception):
    pass
class CustomerNotFoundError(CustomerDAOException):
    pass
class CustomerDatabaseError(CustomerDAOException):
    pass

class Customer:
    def __init__(self, db_connection):
        self.conn = db_connection.get_connection()

    def create_customer(self, name, surname, email, tel):
        cursor = None
        try:
            cursor = self.conn.cursor()
            sql = """
            INSERT INTO CUSTOMER(NAME, SURNAME, EMAIL, TEL) VALUES (:name, :surname, :email, :tel)
            """

            cursor.execute(sql, {
                'name': name,
                'surname': surname,
                'email': email,
                'tel': tel,
            })

            self.conn.commit()
        except cx_Oracle.IntegrityError as e:
            self.conn.rollback()
            error_obj, = e.args
            raise CustomerDatabaseError(f"Database error: {error_obj.message}")
        finally:
            if cursor: cursor.close()

    def all_customers(self):
        cursor = None
        try:
            cursor = self.conn.cursor()
            sql = """
            SELECT NAME, SURNAME, EMAIL, TEL FROM CUSTOMER
            """

            cursor.execute(sql)
            result = cursor.fetchall()
            return result

        except cx_Oracle.DatabaseError as e:
            error_obj, = e.args
            raise CustomerDatabaseError(f"Database error retrieving customers: {error_obj.message}")

        finally:
            if cursor:
                cursor.close()


    def all_customers_with_ids(self):
        cursor = None
        try:
            cursor = self.conn.cursor()
            sql = """
            SELECT ID, NAME, SURNAME, EMAIL, TEL FROM customer ORDER BY ID
            """

            cursor.execute(sql)
            result = cursor.fetchall()
            return result

        except cx_Oracle.DatabaseError as e:
            error_obj, = e.args
            raise CustomerDatabaseError(f"Database error retrieving customers: {error_obj.message}")
        finally:
            if cursor:
                cursor.close()

    def select_customer_by_id(self, id):
        cursor = None
        try:
            cursor = self.conn.cursor()
            sql = """
            SELECT NAME, SURNAME, EMAIL, TEL FROM CUSTOMER WHERE ID = :id
            """

            cursor.execute(sql, {
                "id": id
            })
            result = cursor.fetchone()
            if result is None:
                raise CustomerNotFoundError(f"Customer with ID: {id} not found")

            return result

        except CustomerNotFoundError:
            raise

        finally:
            if cursor:
                cursor.close()

    def select_customer_by_email(self, email):
        cursor = None
        try:
            cursor = self.conn.cursor()
            sql = """
            SELECT ID, NAME, SURNAME, EMAIL, TEL
            FROM customer
            WHERE LOWER(email) = LOWER(:email)
            """

            cursor.execute(sql, {
                "email": email
            })
            result = cursor.fetchone()
            if result is None:
                raise CustomerNotFoundError(f"Customer with email: {email} not found")

            return result
        except CustomerNotFoundError:
            raise

        finally:
            if cursor:
                cursor.close()

    def update_customer(self, id, name=None, surname=None, email=None, tel=None):
        cursor = None
        try:
            cursor = self.conn.cursor()

            cursor.execute("SELECT ID FROM CUSTOMER WHERE ID = :id", {"id": id})
            if not cursor.fetchone():
                raise CustomerNotFoundError(f"Customer {id} not found")

            fields = {
                "NAME": name,
                "SURNAME": surname,
                "EMAIL": email,
                "TEL": tel,
            }

            update_fields = {k: v for k, v in fields.items() if v is not None}

            if not update_fields:
                return

            set_clause = ", ".join([f"{key} = :{key}" for key in update_fields])

            sql = f"""
            UPDATE customer SET {set_clause} 
            WHERE ID = :id
            """

            update_fields["id"] = id
            cursor.execute(sql, update_fields)
            self.conn.commit()
        except cx_Oracle.IntegrityError as e:
            self.conn.rollback()
            raise CustomerDatabaseError("Email or phone number conflict.")
        finally:
            if cursor:
                cursor.close()

    def delete_customer(self, id):
        cursor = None
        try:
            cursor = self.conn.cursor()
            sql = """
            DELETE FROM CUSTOMER WHERE ID = :id
            """

            cursor.execute(sql, {"id": id})
            self.conn.commit()
        except cx_Oracle.IntegrityError:
            self.conn.rollback()
            raise CustomerDatabaseError("Cannot delete customer: they have active or past rentals.")
        finally:
            if cursor: cursor.close()
