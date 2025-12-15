import cx_Oracle

class Database:
    _instance = None

    def __new__(cls, config):
        if cls._instance is None:
            cls._instance = super(Database, cls).__new__(cls)
            cls._instance._config = config
            cls._instance.conn = None
        return cls._instance

    def _connect_if_needed(self):
        if self.conn is None:
            dsn = f"{self._config['host']}:{self._config['port']}/{self._config['service_name']}"
            self.conn = cx_Oracle.connect(
                user=self._config['user'],
                password=self._config['password'],
                dsn=dsn
            )
            print("Database connection Initialized.")

    def get_connection(self):
        self._connect_if_needed()
        return self.conn

    def close(self):
        if self.conn:
            self.conn.close()
            self.conn = None
            type(self)._instance = None
