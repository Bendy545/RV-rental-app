class Rv:
    def __init__(self, db_connection):
        self.conn = db_connection.get_connection()

    def create_rv(self, spz, manufacture_date, price_for_day, status, id_brand, id_type):
        cursor = self.conn.cursor()
        sql = """
        INSERT INTO rv(SPZ, MANUFACTURE_DATE, PRICE_FOR_DAY, STATUS, ID_BRAND, ID_TYPE)
        VALUES (:spz, :manufacture_date, :price_for_day, :status, :id_brand, :id_type)
        """

        cursor.execute(sql, {
            'spz': spz,
            'manufacture_date': manufacture_date,
            'price_for_day': price_for_day,
            'status': status,
            'id_brand': id_brand,
            'id_type': id_type
        })

        self.conn.commit()
        cursor.close()

    def all_rvs(self):
        cursor = self.conn.cursor()
        sql = """
        SELECT rv.ID, rv.SPZ, rv.MANUFACTURE_DATE, rv.PRICE_FOR_DAY, rv.STATUS, b.NAME AS BRAND, t.NAME AS TYPE
        FROM rv
        JOIN brand b ON rv.ID_BRAND = b.ID
        JOIN rv_type t ON rv.ID_TYPE = t.ID
        """

        cursor.execute(sql)
        result = cursor.fetchall()
        cursor.close()
        return result

    def update_rv(self, spz=None, manufacture_date=None, price_for_day=None, status=None, id_brand=None, id_type=None):
        cursor = self.conn.cursor()

        if spz is not None:
            cursor.execute("""UPDATE rv SET SPZ = :spz WHERE ID = :id""", {"spz": spz, "id": id})
        if manufacture_date is not None:
            cursor.execute("""UPDATE rv SET MANUFACTURE_DATE = :date WHERE ID = :id""",{"date": manufacture_date, "id": id})
        if price_for_day is not None:
            cursor.execute("""UPDATE rv SET PRICE_FOR_DAY = :price WHERE ID = :id""", {"price": price_for_day, "id": id})
        if status is not None:
            cursor.execute("""UPDATE rv SET STATUS = :status WHERE ID = :id""", {"status": status, "id": id})
        if id_brand is not None:
            cursor.execute("""UPDATE rv SET ID_BRAND = :id_brand WHERE ID = :id""", {"id_brand": id_brand, "id": id})
        if id_type is not None:
            cursor.execute("""UPDATE rv SET ID_TYPE = :id_type WHERE ID = :id""", {"id_type": id_type, "id": id})

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
