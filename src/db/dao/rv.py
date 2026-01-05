import cx_Oracle

class RvDAOException(Exception):
    pass
class RvNotFoundError(RvDAOException):
    pass
class RvDatabaseError(RvDAOException):
    pass

class Rv:
    def __init__(self, db_connection):
        self.conn = db_connection.get_connection()

    def create_rv(self, spz, manufacture_date, price_for_day, id_brand, id_type):
        cursor = None
        try:
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
        except cx_Oracle.IntegrityError as e:
            self.conn.rollback()
            error_obj, = e.args
            if error_obj.code == 1:  # Unique SPZ
                raise RvDatabaseError(f"SPZ '{spz}' is already registered.")
            raise RvDatabaseError(f"Database error: {error_obj.message}")
        finally:
            if cursor:
                cursor.close()

    def all_rvs(self):
        cursor = None
        try:
            cursor = self.conn.cursor()
            sql = """
            SELECT rv.ID, rv.SPZ, rv.MANUFACTURE_DATE, rv.PRICE_FOR_DAY, b.NAME AS BRAND, t.NAME AS TYPE
            FROM rv
            JOIN brand b ON rv.ID_BRAND = b.ID
            JOIN rv_type t ON rv.ID_TYPE = t.ID
            """

            cursor.execute(sql)
            result = cursor.fetchall()
            return result
        except cx_Oracle.DatabaseError as e:
            error_obj, = e.args
            raise RvDatabaseError(f"Database error retrieving Rvs: {error_obj.message}")

        finally:
            if cursor:
                cursor.close()

    def select_rv_by_id(self, id):
        cursor = None
        try:
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
            if result is None:
                raise RvNotFoundError(f"RV eith ID '{id}' not found.")

            return result

        except RvNotFoundError:
            raise

        finally:
            if cursor:
                cursor.close()

    def check_availability(self, id, date_from, date_to):
        cursor = self.conn.cursor()
        sql = """
        SELECT COUNT(*) 
        FROM rental
        WHERE id_rv = :id AND status IN ('reserved', 'active') AND NOT (:date_to <= date_from OR :date_from >= date_to)
        """

        cursor.execute(sql, {
            'rv_id': id,
            'date_from': date_from,
            'date_to': date_to
        })
        count = cursor.fetchone()[0]
        cursor.close()
        return count == 0

    def count_rvs_by_type(self, type_id):
        cursor = self.conn.cursor()
        sql = """
        SELECT COUNT(*)
        FROM rv
        WHERE id_type = :type_id
        """
        cursor.execute(sql, {
            'type_id': type_id
        })
        count = cursor.fetchone()[0]
        cursor.close()
        return count

    def count_rvs_by_brand(self, brand_id):
        cursor = self.conn.cursor()
        sql = """
              SELECT COUNT(*) \
              FROM rv \
              WHERE id_brand = :brand_id \
              """
        cursor.execute(sql, {"brand_id": brand_id})
        count = cursor.fetchone()[0]
        cursor.close()
        return count

    def update_rv(self,id ,spz=None, manufacture_date=None, price_for_day=None, id_brand=None, id_type=None):
        cursor = None
        try:

            cursor = self.conn.cursor()

            cursor.execute("SELECT ID FROM rv WHERE ID = :id", {"id": id})
            if not cursor.fetchone(): raise RvNotFoundError(f"RV with ID {id} not found")

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
        except cx_Oracle.IntegrityError:
            self.conn.rollback()
            raise RvDatabaseError("Update failed: SPZ conflict or invalid references.")
        finally:
            if cursor:
                cursor.close()

    def delete_rv(self, id):
        cursor = None
        try:
            cursor = self.conn.cursor()
            sql = """
            DELETE FROM rv WHERE ID = :id
            """

            cursor.execute(sql, {"id": id})

            self.conn.commit()
        except cx_Oracle.IntegrityError:
            self.conn.rollback()
            raise RvDatabaseError("Cannot delete RV: It has associated rental records.")
        finally:
            if cursor: cursor.close()
