import sqlite3

class DatabaseInterface:
    def __init__(self, db_name: str):
        try:
            self.connection = sqlite3.connect(db_name)
            self.cursor = self.connection.cursor()
        except sqlite3.Error:
            print("Error initializing database")

    def query(self, query: str, params: tuple = ()):
        self.cursor.execute(query, params)

    def commit(self):
        self.connection.commit()

    def close(self):
        self.connection.close()

    def get_all_stations(self):
        """Returns list of stations : tuple (id, station_id, num_lights, status, has_flasher)"""
        try:
            self.cursor.execute("SELECT * FROM stations")
            rows = self.cursor.fetchall()
            
            return rows
        except (sqlite3.Error):
            print("Error loading stations from database.")