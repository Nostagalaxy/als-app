from rich import print
from textual.message import Message

from db_init import DatabaseInterface as DB

class LightField:

    #                                   TODO  
    #       - Set up has_flasher for each station in __load_stations_from_file()
    #       - Create multiple databases for different systems 

    class __Station:

        class _Light:
            # fields (id, station_id, pos, type, color, status, loop)
            def __init__(self, station_id : int, pos : int, type :str,  color : str, status : bool) -> None:
                self.station_id = station_id
                self.pos = pos
                self.type = type
                self.color = color
                self.status = status

            def __str__(self):
                """Return string representation of object"""
                return f"[/Light Station : {self.station_id}, Pos : {self.pos}, Color : {self.color}, Static : {self.status}, Type : {self.type}]"
            
        # Attr : id, station_id, num_lights, status, has_flasher
        def __init__(self, id : int, num_lights : int, status : bool, has_flasher : bool) -> None:
            self.id = id
            self.num_lights = num_lights
            self.status = status
            self.has_flasher = has_flasher
            self.lights : list[LightField.__Station._Light] = []
            self.lights_out : list[LightField.__Station._Light] = []
            self.size : int = 0

        def get_light(self, pos : int) -> "LightField.__Station._Light":
            """Get light from indicated position."""
            return self.lights[pos - 1]
        
        def get_size(self) -> int:
            """Returns number of lights station has."""
            return self.num_lights
        
        def set_status(self, status : bool) -> None:
            self.status = status

        def add_light(self, light_data : tuple) -> None:
            """Add light to station"""
            # fields (id, station_id, pos, type, color, status, loop)
            try:
                pos : int = light_data[2]
                type : str = light_data[3]
                color : str = light_data[4]
                status : bool = light_data[5]
                # TODO Add loop

                cur_light = self._Light(self.id, pos, type, color, status)

                self.lights.append(cur_light)
                self.size += 1

            except ValueError:
                print(f"[bold red]ERROR[/bold red] : Unable to parse light data on station {self.id}")

        def __str__(self):
            """Return string representation of object"""
            return f"[/Station (ID : {self.id}), (Number of Lights : {self.num_lights}), (Status : {self.status}), (Flasher : {self.has_flasher})]"

    def __init__(self, database_file_path : str) -> None:
        self.stations = []
        self.db = DB(database_file_path)
        self.__load_system_db()
        
        #DEBUG
        print('Als Initialized')

    def __load_system_db(self) -> None:
        # Get list of station data from database
        station_data_rows = self.db.get_all_stations()

        # Initialize each station with data from the list
        if station_data_rows is not None:
            for row in station_data_rows:
                try:
                    # Attr : id, station_id, num_lights, status, has_flasher
                    station_id : int = int(row[1])
                    num_lights : int = int(row[2])
                    status : bool = bool(row[3])
                    has_flasher : bool = bool(row[4])

                    cur_station = LightField.__Station(station_id, num_lights, status, has_flasher)

                    # Add to list of stations
                    self.stations.append(cur_station)

                except ValueError:
                    print("[bold red]ERROR[/bold red] : Failed to parse station data from database")

        # Initialize lights into each station
        for i in range (0, 25):
            # Get the current station in list
            cur_station : LightField.__Station = self.stations[i]

            # Get data from the database
            lights_data : list[tuple] | None = self.db.get_lights_from_station(cur_station.id)
            
            # Add the lights to the station
            if lights_data is not None:
                for row in lights_data:
                    cur_station.add_light(row)

    def get_light_data(self, station_id : int, light_pos : int) -> dict:
        # Check if station_id is valid
        if station_id < 0 or station_id >= len(self.stations):
            raise ValueError(f"Invalid station ID: {station_id}. Must be between 0 and {len(self.stations) - 1}.")
        else:
            # Get station
            station : LightField.__Station = self.stations[station_id]
        
        # Check if light position is valid
        if light_pos < 1 or light_pos > station.size:
            raise ValueError(f"Invalid light position: {light_pos}. Must be between 1 and {station.size - 1}.")
        else:
            # Get light from station
            light : LightField.__Station._Light = station.lights[light_pos - 1]

            data = {
                'station_id' : int(light.station_id),
                'pos' : int(light.pos),
                'type' : light.type,
                'color' : light.color,
                'status' : bool(light.status)
            }

        return data

    def get_station_data(self, station_id : int) -> dict:
        # Check if station_id is valid
        if station_id < 0 or station_id >= len(self.stations):
            raise ValueError(f"Invalid station ID: {station_id}. Must be between 0 and {len(self.stations) - 1}.")
        else:
            # Get station
            station : LightField.__Station = self.stations[station_id]
            data = {
                'id' : int(station.id),
                'num_lights' : int(station.num_lights),
                'status' : bool(station.status),
                'has_flasher' : bool(station.has_flasher)
            }

            return data
        
    def set_light_status(self, station_id : int, light_pos : int, status : bool) -> None:
        """Set the status of a light in the database"""
        # Check if station_id is valid
        if station_id < 0 or station_id > len(self.stations):
            raise ValueError(f"Invalid station ID: {station_id}. Must be between 0 and {len(self.stations)}.")
        else:
            # Get station
            station : LightField.__Station = self.stations[station_id]
        
        # Check if light position is valid
        if light_pos < 1 or light_pos > station.size:
            raise ValueError(f"Invalid light position: {light_pos}. Must be between 1 and {station.size}.")
        else:
            # Get light from station
            light : LightField.__Station._Light = station.lights[light_pos - 1]

            # Set light status
            light.status = status

            # Set status in database
            self.db.set_status_of_light(station.id, light.pos, status)

    # DEBUGGING METHOD
    def print_lights_from_station(self, station_id: int) -> None:
        """Prints the light data for a given station"""
        try:
            if station_id < 0 or station_id >= len(self.stations):
                raise ValueError(f"Invalid station ID: {station_id}. Must be between 0 and {len(self.stations) - 1}.")
            
            station : LightField.__Station = self.stations[station_id]
            print(f"Lights for Station {station.id}:")
            for light in station.lights:
                print(light)
        
        except ValueError as e:
            print(f"[bold red]ERROR[/bold red] : {e}")

    def __str__(self):
        """Return string representation of object"""
        print("+++++++++++++++++ Stations ++++++++++++++++\n")
        for station in self.stations:
            print(station)
        
        print("\n+++++++++++++++++ Lights ++++++++++++++++\n")
        for station in self.stations:
            for light in station.lights:
                print(light)
        return ""
        

    