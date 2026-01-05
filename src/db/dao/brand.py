import cx_Oracle

class BrandDAOException(Exception):
    pass

class BrandNotFoundError(BrandDAOException):
    pass

class BrandDatabaseError(BrandDAOException):
    pass

class Brand:
    def __init__(self, db_connection):
        self.conn = db_connection.get_connection()

    def create_brand(self, name):
        cursor = None
        try:
            cursor = self.conn.cursor()
            sql = """
            INSERT INTO brand (NAME) VALUES (:name)
            """

            cursor.execute(sql, {"name":name})

            self.conn.commit()
        except cx_Oracle.IntegrityError as e:
            self.conn.rollback()
            error_obj, = e.args
            if error_obj.code == 1:
                raise BrandDatabaseError(f"Brand '{name}' already exists")
            raise BrandDatabaseError(f"Database error: {error_obj.message}")
        finally:
            if cursor:
                cursor.close()

    def all_brands(self):
        cursor = None
        try:
            cursor = self.conn.cursor()
            sql = """
            SELECT NAME FROM brand
            """

            cursor.execute(sql)
            result = cursor.fetchall()
            return result
        except cx_Oracle.DatabaseError as e:
            error_obj, = e.args
            raise BrandDatabaseError(f"Database error retrieving brands: {error_obj.message}")

        finally:
            if cursor:
                cursor.close()

    def select_brands_with_ids(self):
        cursor = None
        try:
            cursor = self.conn.cursor()
            sql = """
            SELECT ID, NAME FROM brand ORDER BY NAME
            """

            cursor.execute(sql)
            result = cursor.fetchall()
            return result

        except cx_Oracle.DatabaseError as e:
            error_obj, = e.args
            raise BrandDatabaseError(f"Database error retrieving brands: {error_obj.message}")

        finally:
            if cursor:
                cursor.close()

    def select_brand_by_id(self, id):
        cursor = None
        try:
            cursor = self.conn.cursor()
            sql = """
            SELECT NAME FROM brand WHERE ID = :id
            """
            cursor.execute(sql, {"id":id})
            result = cursor.fetchone()
            if result is None:
                raise BrandNotFoundError(f"Brand with ID: {id} not found")

            return result

        except BrandNotFoundError:
            raise

        finally:
            if cursor:
                cursor.close()

    def update_brand(self, id, name=None):
        cursor = None
        try:
            cursor = self.conn.cursor()

            cursor.execute("SELECT ID FROM brand WHERE ID = :id", {'id': id})
            if cursor.fetchone() is None:
                raise BrandNotFoundError(f"Brand with ID {id} not found")

            if name is not None:
                cursor.execute("""
                UPDATE brand SET NAME = :name WHERE ID = :id
                """, {"name":name, "id":id})

            self.conn.commit()

        except BrandNotFoundError:
            self.conn.rollback()
            raise

        except cx_Oracle.IntegrityError as e:
            self.conn.rollback()
            error_obj, = e.args
            if error_obj.code == 1:
                raise BrandDatabaseError(f"Brand with name '{name}' already exists")
            else:
                raise BrandDatabaseError(f"Database integrity error: {error_obj.message}")

        except cx_Oracle.Error as e:
            self.conn.rollback()
            raise BrandDatabaseError(f"Database error occurred: {str(e)}")

        finally:
            if cursor:
                cursor.close()

    def delete_brand(self, id):
        cursor = None
        try:
            cursor = self.conn.cursor()
            sql = """
            DELETE FROM brand WHERE ID = :id
            """

            cursor.execute(sql, {"id":id})
            self.conn.commit()

        except cx_Oracle.IntegrityError as e:
            self.conn.rollback()
            error_obj, = e.args
            if error_obj.code == 2292:  # Child record found
                raise BrandDatabaseError("Cannot delete brand - it is used by RVs")
            raise BrandDatabaseError(f"Database error: {error_obj.message}")
        finally:
            if cursor: cursor.close()