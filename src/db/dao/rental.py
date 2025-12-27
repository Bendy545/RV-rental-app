class RentalException(Exception):
    pass

class Rental:
    def __init__(self, db_connection):
        self.conn = db_connection.get_connection()

    def create_rental(self, date_from, date_to, creation_date, price, id_customer, id_rv, accessories_list=None):
        cursor = self.conn.cursor()

        try:
            if not accessories_list:
                sql = """
                BEGIN
                create_rental_simple(:date_from, :date_to, :creation_date, :price, :id_customer, :id_rv);
                END;
                """

                cursor.execute(sql, {
                    "date_from": date_from,
                    "date_to": date_to,
                    "creation_date": creation_date,
                    "price": price,
                    "id_customer": id_customer,
                    "id_rv": id_rv
                })
                self.conn.commit()
                print("Rental created successfully (no accessories)")
                return None

            else:
                rental_id = cursor.var(int)
                sql = """
                BEGIN
                create_rental_with_acc(:date_from, :date_to, :creation_date, :price, :id_customer, :id_rv, :rental_id);
                END;
                """

                cursor.execute(sql, {
                    "date_from": date_from,
                    "date_to": date_to,
                    "creation_date": creation_date,
                    "price": price,
                    "id_customer": id_customer,
                    "id_rv": id_rv,
                    "rental_id": rental_id
                })

                rental_id_value = rental_id.getvalue()

                for acc in accessories_list:
                    cursor.execute("""
                           INSERT INTO accessory_rental (id_accessory, id_rental, amount, price_at_rent)
                           VALUES (:id_accessory, :id_rental, :amount, :price)
                           """, {
                               "id_accessory": acc['id_accessory'],
                               "id_rental": rental_id_value,
                               "amount": acc['amount'],
                               "price": acc['price']
                           })

                self.conn.commit()
                print(f"Rental created with {len(accessories_list)} accessories (rental_id: {rental_id_value})")
                return rental_id_value

        except Exception as e:
            self.conn.rollback()
            raise RentalException(f"Error creating rental: {e}")
        finally:
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

    def select_rental_with_accessories(self, id):
        cursor = self.conn.cursor()

        sql = """
        SELECT r.DATE_FROM, r.DATE_TO, r.CREATION_DATE, r.PRICE, r.STATUS, r.IS_PAID, c.EMAIL, rv.SPZ
        FROM rental r 
        JOIN CUSTOMER c ON r.ID_CUSTOMER = c.ID
        JOIN rv ON r.ID_RV = rv.ID
        WHERE r.ID = :id
        """

        cursor.execute(sql, {
            "id": id,
        })
        rental = cursor.fetchone()
        if not rental:
            cursor.close()
            return None

        acc_sql = """
        SELECT a.NAME, ar.AMOUNT, ar.PRICE_AT_RENT
        FROM accessory_rental ar
        JOIN accessory a ON ar.ID_ACCESSORY = a.ID
            WHERE ar.ID_RENTAL = :id
        """

        cursor.execute(acc_sql, {
            "id": id,
        })
        accessories = cursor.fetchall()
        cursor.close()

        return {
            "rental": rental,
            "accessories": accessories
        }

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

    def all_rentals_with_ids(self):
        cursor = self.conn.cursor()
        sql = """
        SELECT r.ID, r.DATE_FROM, r.DATE_TO, r.CREATION_DATE, r.PRICE, r.STATUS, r.IS_PAID, c.EMAIL, rv.SPZ
        FROM rental r 
        JOIN CUSTOMER c ON r.ID_CUSTOMER = c.ID
        JOIN rv ON r.ID_RV = rv.ID
        ORDER BY r.CREATION_DATE DESC
        """

        cursor.execute(sql)
        result = cursor.fetchall()
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
        BEGIN delete_rental_proc(:id); END;
        """
        try:
            cursor.execute(sql, {"id": id})
            self.conn.commit()
        except RentalException as e:
            self.conn.rollback()
            raise e
        finally:
            cursor.close()