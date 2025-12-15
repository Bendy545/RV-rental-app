class Authors:
    def __init__(self, db_connection):
        self.conn = db_connection.get_connection()