class Rv:
    def __init__(self, db_connection):
        self.conn = db_connection.get_connection()

    def create_rv(self, spz, manufacture_date, price_for_day, id_brand, id_type):
        cursor = self.conn.cursor()
        sql = """
        INSERT INTO rv(SPZ, MANUFACTURE_DATE, PRICE_FOR_DAY, ID_BRAND, ID_TYPE)
        VALUES (:spz, :manufacture_date, :price_for_day, :id_brand, :id_type)
        """

        cursor.execute(sql, {
            'spz': spz,
            'manufacture_date': manufacture_date,
            'price_for_day': price_for_day,
            'id_brand': id_brand,
            'id_type': id_type
        })

        self.conn.commit()
        cursor.close()

    def all_rvs(self):
        cursor = self.conn.cursor()
        sql = """
        SELECT rv.ID, rv.SPZ, rv.MANUFACTURE_DATE, rv.PRICE_FOR_DAY, b.NAME AS BRAND, t.NAME AS TYPE
        FROM rv
        JOIN brand b ON rv.ID_BRAND = b.ID
        JOIN rv_type t ON rv.ID_TYPE = t.ID
        """

        cursor.execute(sql)
        result = cursor.fetchall()
        cursor.close()
        return result

    def select_rv_by_id(self, id):
        cursor = self.conn.cursor()
        sql = """
        SELECT rv.SPZ, rv.MANUFACTURE_DATE, rv.PRICE_FOR_DAY, b.NAME AS BRAND, t.NAME AS TYPE
        FROM rv
        JOIN brand b on rv.ID_BRAND = b.ID
        JOIN rv_type t ON rv.ID_TYPE = t.ID
        WHERE rv.ID = :id
        """

        cursor.execute(sql, {
            'id': id
        })
        result = cursor.fetchone()
        cursor.close()
        return result

    def update_rv(self, spz=None, manufacture_date=None, price_for_day=None, id_brand=None, id_type=None):
        cursor = self.conn.cursor()

        fields = {
            "SPZ": spz,
            "MANUFACTURE_DATE": manufacture_date,
            "PRICE_FOR_DAY": price_for_day,
            "ID_BRAND": id_brand,
            "ID_TYPE": id_type
        }

        update_fields = {k: v for k, v in fields.items() if v is not None}

        if not update_fields:
            return

        set_clause = ", ".join([f"{key} = :{key}" for key in update_fields])

        sql = f"""
        UPDATE rv SET {set_clause} 
        WHERE ID = :id
        """

        update_fields["id"] = id
        cursor.execute(sql, update_fields)
        self.conn.commit()
        cursor.close()

    def delete_rv(self, id):
        cursor = self.conn.cursor()
        sql = """
        DELETE FROM rv WHERE ID = :id
        """

        cursor.execute(sql, {"id": id})

        self.conn.commit()
        cursor.close()
