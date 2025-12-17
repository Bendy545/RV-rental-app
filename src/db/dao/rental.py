class Rental:
    def __init__(self, db_connection):
        self.conn = db_connection.get_connection()

    def create_rental(self, date_from, date_to, creation_date, price, status, is_paid, id_customer, id_rv):
        cursor = self.conn.cursor()
        sql = """
        INSERT INTO rental (DATE_FROM, DATE_TO, CREATION_DATE, PRICE, STATUS, IS_PAID, ID_CUSTOMER, ID_RV)
        VALUES (:date_from, :date_to, :creation_date, :price, :status, :is_paid, :id_customer, :id_rv)
        """

        cursor.execute(sql, {
            "date_from": date_from,
            "date_to": date_to,
            "creation_date": creation_date,
            "price": price,
            "status": status,
            "is_paid": is_paid,
            "id_customer": id_customer,
            "id_rv": id_rv
        })
        self.conn.commit()
        cursor.close()

    def all_rentals(self):
        cursor = self.conn.cursor()
        sql = """
        SELECT r.DATE_FROM, r.DATE_TO, r.CREATION_DATE, r.PRICE, r.STATUS, r.IS_PAID, c.EMAIL, rv.SPZ
        FROM rental r 
        JOIN CUSTOMER c ON r.ID_CUSTOMER = c.ID
        JOIN rv ON r.ID_RV = rv.ID
        """

        cursor.execute(sql)
        result = cursor.fetchall()
        cursor.close()
        return result

    def select_rental_by_id(self, id):
        cursor = self.conn.cursor()
        sql = """
        SELECT r.DATE_FROM, r.DATE_TO, r.CREATION_DATE, r.PRICE, r.STATUS, r.IS_PAID, c.EMAIL, rv.SPZ
        FROM rental r 
        JOIN CUSTOMER c ON r.ID_CUSTOMER = c.ID
        JOIN rv ON r.ID_RV = rv.ID
        WHERE r.ID = :id
        """

        cursor.execute(sql, {"id": id})
        result = cursor.fetchone()
        cursor.close()
        return result

    def update_rental(self, id, date_from=None, date_to=None, price=None, status=None, is_paid=None, id_customer=None, id_rv=None):
        cursor = self.conn.cursor()

        fields = {
            "DATE_FROM": date_from,
            "DATE_TO": date_to,
            "PRICE": price,
            "STATUS": status,
            "IS_PAID": is_paid,
            "ID_CUSTOMER": id_customer,
            "ID_RV": id_rv
        }

        update_fields = {k: v for k, v in fields.items() if v is not None}

        if not update_fields:
            return

        set_clause = ", ".join([f"{key} = :{key}" for key in update_fields])

        sql = f"""
        UPDATE rental SET {set_clause} 
        WHERE ID = :id
        """

        update_fields["id"] = id
        cursor.execute(sql, update_fields)
        self.conn.commit()
        cursor.close()

    def delete_rental(self, id):
        cursor = self.conn.cursor()
        sql = """
        DELETE FROM rental WHERE ID = :id
        """

        cursor.execute(sql, {"id": id})
        self.conn.commit()
        cursor.close()