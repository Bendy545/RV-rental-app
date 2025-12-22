class Accessory:
    def __init__(self, db_connection):
        self.conn = db_connection.get_connection()

    def create_accessory(self, name, description, price_for_day):
        cursor = self.conn.cursor()
        sql = """
        INSERT INTO accessory (NAME, DESCRIPTION, PRICE_FOR_DAY) VALUES (:name, :description, :price_for_day)
        """

        cursor.execute(sql, {
            'name': name,
            'description': description,
            'price_for_day': price_for_day
        })
        self.conn.commit()
        cursor.close()

    def all_accessories(self):
        cursor = self.conn.cursor()
        sql = """
        SELECT NAME, DESCRIPTION, PRICE_FOR_DAY FROM accessory
        """

        cursor.execute(sql)
        result = cursor.fetchall()
        cursor.close()
        return result

    def select_accessory_by_id(self, id):
        cursor = self.conn.cursor()
        sql = """
        SELECT NAME, DESCRIPTION, PRICE_FOR_DAY FROM accessory WHERE ID = :id
        """

        cursor.execute(sql, {
            'id': id
        })
        result = cursor.fetchone()
        cursor.close()
        return result

    def update_accessory(self, id, name=None, description=None, price_for_day=None):
        cursor = self.conn.cursor()

        fields = {
            "NAME": name,
            "DESCRIPTION": description,
            "PRICE_FOR_DAY": price_for_day
        }

        update_fields = {k: v for k, v in fields.items() if v is not None}

        if not update_fields:
            return

        set_clause = ", ".join([f"{key} = :{key}" for key in update_fields])

        sql = f"""
        UPDATE accessory SET {set_clause} 
        WHERE ID = :id
        """

        update_fields["id"] = id
        cursor.execute(sql, update_fields)
        self.conn.commit()
        cursor.close()

    def delete_accessory(self, id):
        cursor = self.conn.cursor()
        sql = """
        DELETE FROM accessory WHERE ID = :id
        """

        cursor.execute(sql, {"id": id})
        self.conn.commit()
        cursor.close()
