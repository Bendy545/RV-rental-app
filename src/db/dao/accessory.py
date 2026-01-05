import cx_Oracle

class AccessoryDAOException(Exception):
    pass

class AccessoryNotFoundError(AccessoryDAOException):
    pass

class AccessoryDatabaseError(AccessoryDAOException):
    pass

class Accessory:
    def __init__(self, db_connection):
        self.conn = db_connection.get_connection()

    def create_accessory(self, name, description, price_for_day):
        cursor = None
        try:
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

        except cx_Oracle.IntegrityError as e:
            self.conn.rollback()
            error_obj, = e.args
            if error_obj.code == 1:
                raise AccessoryDatabaseError(f"Accessory with name '{name}' already exists")
            else:
                raise AccessoryDatabaseError(f"Integrity constraint violated: {error_obj.message}")

        finally:
            if cursor:
                cursor.close()

    def all_accessories(self):
        cursor = None
        try:
            cursor = self.conn.cursor()
            sql = """
            SELECT NAME, DESCRIPTION, PRICE_FOR_DAY FROM accessory
            """

            cursor.execute(sql)
            result = cursor.fetchall()
            return result

        except cx_Oracle.DatabaseError as e:
            error_obj, = e.args
            raise AccessoryDatabaseError(f"Database error retrieving accessories: {error_obj.message}")

        finally:
            if cursor:
                cursor.close()

    def all_accessories_with_ids(self):
        cursor = None
        try:
            cursor = self.conn.cursor()
            sql = """
            SELECT ID, NAME, DESCRIPTION, PRICE_FOR_DAY FROM accessory ORDER BY ID
            """

            cursor.execute(sql)
            result = cursor.fetchall()
            return result

        except cx_Oracle.DatabaseError as e:
            error_obj, = e.args
            raise AccessoryDatabaseError(f"Database error retrieving accessories: {error_obj.message}")

        finally:
            if cursor:
                cursor.close()

    def select_accessory_by_id(self, id):
        cursor = None
        try:
            cursor = self.conn.cursor()
            sql = """
            SELECT NAME, DESCRIPTION, PRICE_FOR_DAY FROM accessory WHERE ID = :id
            """

            cursor.execute(sql, {
                'id': id
            })
            result = cursor.fetchone()
            if result is None:
                raise AccessoryNotFoundError(f"Accessory with ID {id} not found")

            return result

        except AccessoryNotFoundError:
            raise

        finally:
            if cursor:
                cursor.close()

    def update_accessory(self, id, name=None, description=None, price_for_day=None):
        cursor = None
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT ID FROM accessory WHERE ID = :id", {'id': id})
            if cursor.fetchone() is None:
                raise AccessoryNotFoundError(f"Accessory with ID {id} not found")

            fields = {
                "NAME": name,
                "DESCRIPTION": description,
                "PRICE_FOR_DAY": price_for_day
            }

            update_fields = {k: v for k, v in fields.items() if v is not None}

            if not update_fields:
                return

            set_clause = ", ".join([f"{key} = :{key}" for key in update_fields])
            sql = f"UPDATE accessory SET {set_clause} WHERE ID = :id"

            update_fields["id"] = id
            cursor.execute(sql, update_fields)
            self.conn.commit()

        except AccessoryNotFoundError:
            self.conn.rollback()
            raise

        except cx_Oracle.IntegrityError as e:
            self.conn.rollback()
            error_obj, = e.args
            if error_obj.code == 1:
                raise AccessoryDatabaseError(f"Accessory with name '{name}' already exists")
            else:
                raise AccessoryDatabaseError(f"Integrity constraint violated: {error_obj.message}")

        finally:
            if cursor:
                cursor.close()

    def delete_accessory(self, id):
        cursor = None
        try:
            cursor = self.conn.cursor()

            cursor.execute("SELECT ID FROM accessory WHERE ID = :id", {'id': id})
            if cursor.fetchone() is None:
                raise AccessoryNotFoundError(f"Accessory with ID {id} not found")

            sql = "DELETE FROM accessory WHERE ID = :id"
            cursor.execute(sql, {"id": id})
            self.conn.commit()

        except AccessoryNotFoundError:
            self.conn.rollback()
            raise

        except cx_Oracle.IntegrityError as e:
            self.conn.rollback()
            error_obj, = e.args
            if error_obj.code == 2292:
                raise AccessoryDatabaseError(
                    "Cannot delete accessory because it is referenced in active rentals. "
                    "Please remove associated rentals first."
                )
            else:
                raise AccessoryDatabaseError(f"Integrity constraint violated: {error_obj.message}")

        finally:
            if cursor:
                cursor.close()
