import cx_Oracle

class RvTypeDAOException(Exception):
    pass
class RvTypeNotFoundError(RvTypeDAOException):
    pass
class RvTypeDatabaseError(RvTypeDAOException):
    pass

class RvType:
    def __init__(self, db_connection):
        self.conn = db_connection.get_connection()

    def create_type(self, name, description):
        cursor = None
        try:
            cursor = self.conn.cursor()
            sql = """
            INSERT INTO rv_type(NAME, DESCRIPTION) VALUES (:name, :description)
            """

            cursor.execute(sql, {
                'name': name,
                'description': description
            })
            self.conn.commit()
        except cx_Oracle.IntegrityError as e:
            self.conn.rollback()
            error_obj, = e.args
            raise RvTypeDatabaseError(f"Database error: {error_obj.message}")
        finally:
            if cursor: cursor.close()

    def all_types(self):
        cursor = None
        try:
            cursor = self.conn.cursor()
            sql = """
            SELECT NAME, DESCRIPTION FROM rv_type
            """

            cursor.execute(sql)
            result = cursor.fetchall()
            return result
        except cx_Oracle.DatabaseError as e:
            error_obj, = e.args
            raise RvTypeDatabaseError(f"Database error retrieving rv_types: {error_obj.message}")

        finally:
            if cursor:
                cursor.close()

    def select_types_with_ids(self):
        cursor = None
        try:
            cursor = self.conn.cursor()
            sql = """
            SELECT ID, NAME, DESCRIPTION FROM rv_type ORDER BY NAME
            """

            cursor.execute(sql)
            result = cursor.fetchall()
            return result

        except cx_Oracle.DatabaseError as e:
            error_obj, = e.args
            raise RvTypeDatabaseError(f"Database error retrieving rv_types: {error_obj.message}")
        finally:
            if cursor:
                cursor.close()

    def select_type_by_id(self, id):
        cursor = None
        try:
            cursor = self.conn.cursor()
            sql = """
            SELECT NAME, DESCRIPTION FROM rv_type WHERE ID = :id
            """

            cursor.execute(sql, {
                'id': id
            })
            result = cursor.fetchone()
            if result is None:
                raise RvTypeNotFoundError(f"RV Type with ID: {id} not found")

            return result

        except RvTypeNotFoundError:
            raise

        finally:
            if cursor:
                cursor.close()

    def update_type(self, id, name=None, description=None):
        cursor = None
        try:

            cursor = self.conn.cursor()
            cursor.execute("SELECT ID FROM rv_type WHERE ID = :id", {'id': id})
            if not cursor.fetchone():
                raise RvTypeNotFoundError(f"RV type {id} not found")

            if name:
                cursor.execute("""
                UPDATE rv_type SET NAME = :name WHERE ID = :id
                """, {"name":name, "id":id})

            if description:
                cursor.execute("""
                UPDATE rv_type SET DESCRIPTION = :description WHERE ID = :id
                """, {"description":description, "id":id})

            self.conn.commit()
        except cx_Oracle.Error as e:
            self.conn.rollback()
            raise RvTypeDatabaseError(f"Update failed: {str(e)}")
        finally:
            if cursor:
                cursor.close()

    def delete_type(self, id):
        cursor = None
        try:

            cursor = self.conn.cursor()
            sql = """
            DELETE FROM rv_type WHERE ID = :id
            """

            cursor.execute(sql, {"id":id})
            self.conn.commit()
        except cx_Oracle.IntegrityError:
            self.conn.rollback()
            raise RvTypeDatabaseError("Cannot delete type: it is assigned to existing RVs.")
        finally:
            if cursor:
                cursor.close()