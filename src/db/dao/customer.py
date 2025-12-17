class Customer:
    def __init__(self, db_connection):
        self.conn = db_connection.get_connection()

    def create_customer(self, name, surname, email, tel):
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
        cursor.close()

    def all_customers(self):
        cursor = self.conn.cursor()
        sql = """
        SELECT NAME, SURNAME, EMAIL, TEL FROM CUSTOMER
        """

        cursor.execute(sql)
        result = cursor.fetchall()
        cursor.close()
        return result

    def select_customer_by_id(self, id):
        cursor = self.conn.cursor()
        sql = """
        SELECT NAME, SURNAME, EMAIL, TEL FROM CUSTOMER WHERE ID = :id
        """

        cursor.execute(sql, {
            "id": id
        })
        result = cursor.fetchone()
        cursor.close()
        return result

    def update_customer(self, id, name=None, surname=None, email=None, tel=None):
        cursor = self.conn.cursor()

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
        cursor.close()

    def delete_customer(self, id):
        cursor = self.conn.cursor()
        sql = """
        DELETE FROM CUSTOMER WHERE ID = :id
        """

        cursor.execute(sql, {"id": id})
        self.conn.commit()
        cursor.close()