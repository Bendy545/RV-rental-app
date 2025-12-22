class Brand:
    def __init__(self, db_connection):
        self.conn = db_connection.get_connection()

    def create_brand(self, name):
        cursor = self.conn.cursor()
        sql = """
        INSERT INTO brand (NAME) VALUES (:name)
        """

        cursor.execute(sql, {"name":name})

        self.conn.commit()
        cursor.close()

    def all_brands(self):
        cursor = self.conn.cursor()
        sql = """
        SELECT NAME FROM brand
        """

        cursor.execute(sql)
        result = cursor.fetchall()
        cursor.close()
        return result

    def select_brands_with_ids(self):
        cursor = self.conn.cursor()
        sql = """
        SELECT ID, NAME FROM brand ORDER BY NAME
        """

        cursor.execute(sql)
        result = cursor.fetchall()
        cursor.close()
        return result

    def select_brand_by_id(self, id):
        cursor = self.conn.cursor()
        sql = """
        SELECT NAME FROM brand WHERE ID = :id
        """
        cursor.execute(sql, {"id":id})
        result = cursor.fetchone()
        cursor.close()
        return result

    def update_brand(self, id, name=None):
        cursor = self.conn.cursor()

        if name is not None:
            cursor.execute("""
            UPDATE brand SET NAME = :name WHERE ID = :id
            """, {"name":name, "id":id})

        self.conn.commit()
        cursor.close()

    def delete_brand(self, id):
        cursor = self.conn.cursor()
        sql = """
        DELETE FROM brand WHERE ID = :id
        """

        cursor.execute(sql, {"id":id})
        self.conn.commit()
        cursor.close()