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

    def set_status_of_light(self, station_id : int, light_pos : int, status : bool) -> None:
        """Set the status of a light in the database"""
        try:
            # Check if the station exists
            self.cursor.execute("SELECT * FROM lights WHERE station_id = ? AND position = ?", (station_id, light_pos))
            if not self.cursor.fetchone():
                print(f"ERROR : No light found at position {light_pos} on station {station_id}")
                return
            
            # Update the status of the light
            self.cursor.execute("UPDATE lights SET status = ? WHERE station_id = ? AND position = ?", (status, station_id, light_pos))
            self.commit()

            # Debug message
            print('Light status updated successfully.')

        except sqlite3.Error:
            print(f"ERROR : Unable to set status of light at position {light_pos} on station {station_id}")


    # Test function to retrieve light data
    def print_light_data(self, station_id: int, light_pos: int) -> None:
        """Prints the light data for a given station and light position"""
        try:
            self.cursor.execute("SELECT * FROM lights WHERE station_id = ? AND position = ?", (station_id, light_pos))
            light_data = self.cursor.fetchone()
            if light_data:
                print(f"Light Data for Station {station_id}, Position {light_pos}: {light_data}")
            else:
                print(f"No data found for Station {station_id}, Position {light_pos}")
        except sqlite3.Error:
            print(f"ERROR : Unable to retrieve light data for station {station_id}, position {light_pos}")