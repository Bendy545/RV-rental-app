class AccessoryRental:
    def __init__(self, db_connection):
        self.conn = db_connection.get_connection()

    def create_accessory_rental(self, id_accessory, id_rental, amount, price_at_rent):
        cursor = self.conn.cursor()
        sql = """
        INSERT INTO accessory_rental (ID_ACCESSORY, ID_RENTAL, AMOUNT, PRICE_AT_RENT)
        VALUES (:id_accessory, :id_rental, :amount, :price_at_rent)
        """

        cursor.execute(sql, {
            "id_accessory": id_accessory,
            "id_rental": id_rental,
            "amount": amount,
            "price_at_rent": price_at_rent,
        })
        self.conn.commit()
        cursor.close()

    def all_accessory_rentals(self):
        cursor = self.conn.cursor()
        sql = """
        SELECT a.NAME, accessory_rental.ID_RENTAL, accessory_rental.AMOUNT, accessory_rental.PRICE_AT_RENT FROM accessory_rental
        JOIN accessory a ON a.ID = accessory_rental.ID_ACCESSORY
        """

        cursor.execute(sql)
        result = cursor.fetchall()
        cursor.close()
        return result

    def select_accessory_rental_by_id(self, id):
        cursor = self.conn.cursor()
        sql = """
        SELECT a.NAME, accessory_rental.ID_RENTAL, accessory_rental.AMOUNT, accessory_rental.PRICE_AT_RENT 
        FROM accessory_rental
        JOIN accessory a ON a.ID = accessory_rental.ID_ACCESSORY
        WHERE accessory_rental.ID = :id
        """

        cursor.execute(sql, {
            "id": id,
        })
        result = cursor.fetchone()
        cursor.close()
        return result

    def update_accessory_rental(self, id, id_accessory=None, id_rental=None, amount=None, price_at_rent=None):
        cursor = self.conn.cursor()

        fields = {
            "ID_ACCESSORY": id_accessory,
            "ID_RENTAL": id_rental,
            "AMOUNT": amount,
            "PRICE_AT_RENT": price_at_rent,
        }

        update_fields = {k: v for k, v in fields.items() if v is not None}

        if not update_fields:
            return

        set_clause = ", ".join([f"{key} = :{key}" for key in update_fields])

        sql = f"""
        UPDATE accessory_rental SET {set_clause} 
        WHERE ID = :id
        """

        update_fields["id"] = id
        cursor.execute(sql, update_fields)
        self.conn.commit()
        cursor.close()

    def delete_accessory_rental(self, id):
        cursor = self.conn.cursor()
        sql = """
        DELETE FROM accessory_rental WHERE ID = :id
        """

        cursor.execute(sql, {
            "id": id,
        })
        self.conn.commit()
        cursor.close()

