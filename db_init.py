import sqlite3

class DatabaseInterface:
    def __init__(self, db_name: str):
        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()
        #self.__create_tables()

    def query(self, query: str, params: tuple = ()):
        self.cursor.execute(query, params)

    def commit(self):
        self.connection.commit()

    def close(self):
        self.connection.close()
