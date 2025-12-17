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

    def update_customer(self, id, name, surname, email, tel):
        cursor = self.conn.cursor()

        if name is not None:
            cursor.execute("""
            UPDATE CUSTOMER SET NAME = :name WHERE ID = :id
            """, {"name": name, "id": id})

        if surname is not None:
            cursor.execute("""
            UPDATE CUSTOMER SET SURNAME = :surname WHERE ID = :id
            """, {"surname": surname, "id": id})

        if email is not None:
            cursor.execute("""
            UPDATE CUSTOMER SET EMAIL = :email WHERE ID = :id
            """, {"email": email, "id": id})

        if tel is not None:
            cursor.execute("""
            UPDATE CUSTOMER SET TEL = :tel WHERE ID = :id
            """, {"tel": tel, "id": id})

    def delete_customer(self, id):
        cursor = self.conn.cursor()
        sql = """
        DELETE FROM CUSTOMER WHERE ID = :id
        """

        cursor.execute(sql, {"id": id})
        self.conn.commit()
        cursor.close()