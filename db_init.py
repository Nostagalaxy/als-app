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
            station_data = self.cursor.fetchall()
            
            return station_data
        
        except sqlite3.Error:
            print("Error loading stations from database.")

    def get_lights_from_station(self, input_station : int) -> list[tuple]| None:
        """Returns a list of lights for a selected station"""
        
        # lights fields :  (id, station_id, pos, type, color, status, loop)
        try:
            self.cursor.execute("SELECT * FROM lights WHERE station_id = ?", (input_station,))
            light_data = self.cursor.fetchall()

            return light_data
        
        except sqlite3.Error:
            print(f"ERROR : Unable load lights for station {input_station}")