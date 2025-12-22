class RvType:
    def __init__(self, db_connection):
        self.conn = db_connection.get_connection()

    def create_type(self, name, description):
        cursor = self.conn.cursor()
        sql = """
        INSERT INTO rv_type(NAME, DESCRIPTION) VALUES (:name, :description)
        """

        cursor.execute(sql, {
            'name': name,
            'description': description
        })
        self.conn.commit()
        cursor.close()

    def all_types(self):
        cursor = self.conn.cursor()
        sql = """
        SELECT NAME, DESCRIPTION FROM rv_type
        """

        cursor.execute(sql)
        result = cursor.fetchall()
        cursor.close()
        return result

    def select_types_with_ids(self):
        cursor = self.conn.cursor()
        sql = """
        SELECT ID, NAME, DESCRIPTION FROM rv_type ORDER BY NAME
        """

        cursor.execute(sql)
        result = cursor.fetchall()
        cursor.close()
        return result

    def select_type_by_id(self, id):
        cursor = self.conn.cursor()
        sql = """
        SELECT NAME, DESCRIPTION FROM rv_type WHERE ID = :id
        """

        cursor.execute(sql, {
            'id': id
        })
        result = cursor.fetchone()
        cursor.close()
        return result

    def update_type(self, id, name=None, description=None):
        cursor = self.conn.cursor()

        if name is not None:
            cursor.execute("""
            UPDATE rv_type SET NAME = :name WHERE ID = :id
            """, {"name":name, "id":id})

        if description is not None:
            cursor.execute("""
            UPDATE rv_type SET DESCRIPTION = :description WHERE ID = :id
            """, {"description":description, "id":id})

        self.conn.commit()
        cursor.close()

    def delete_type(self, id):
        cursor = self.conn.cursor()
        sql = """
        DELETE FROM rv_type WHERE ID = :id
        """

        cursor.execute(sql, {"id":id})
        self.conn.commit()
        cursor.close()