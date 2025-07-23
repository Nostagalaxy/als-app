from rich import print

from db_init import DatabaseInterface as DB

class LightField:

    #                                   TODO  
    #       - Set up has_flasher for each station in __load_stations_from_file()
    #       - Create multiple config files for different systems 

    CONFIG_FILE = "als_config.txt"

    class __Station:

        class __Light:
            # fields (id, station_id, pos, type, color, status, loop)
            def __init__(self, station_id : int, pos : int, type :str,  color : str, status : bool) -> None:
                self.station_id = station_id
                self.pos = pos
                self.type = type
                self.color = color
                self.status = status

            def __str__(self):
                """Return string representation of object"""
                return f"[/Light Station : {self.station_id}, Pos : {self.pos}, Color : {self.color}]"
            
        # Attr : id, station_id, num_lights, status, has_flasher)
        def __init__(self, id : int, num_lights : int, status : bool, has_flasher : bool) -> None:
            self.id = id
            self.num_lights = num_lights
            self.status = status
            self.has_flasher = has_flasher
            self.lights : list[LightField.__Station.__Light] = []
            self.lights_out : list[LightField.__Station.__Light] = []
            self.size : int = 0

        def get_light(self, pos : int) -> "LightField.__Station.__Light":
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

                cur_light = self.__Light(self.id, pos, type, color, status)

                self.lights.append(cur_light)
                self.size += 1

            except ValueError:
                print(f"[bold red]ERROR[/bold red] : Unable to parse light data on station {self.id}")

        def __str__(self):
            """Return string representation of object"""
            return f"[/Station (ID : {self.id}), (Number of Lights : {self.num_lights}), (Status : {self.status}), (Flasher : {self.has_flasher})]"

    def __init__(self, database_file_path : str) -> None:
        self.stations = []
        #self.__load_stations_from_file(self.CONFIG_FILE)
        self.db = DB(database_file_path)
        self.__load_system_db()

    def __load_system_db(self) -> None:
        # Get list of station data from database
        station_data_rows = self.db.get_all_stations()

        # Initialize each station with data from the list
        if station_data_rows is not None:
            for row in station_data_rows:
                
                try:
                    # Attr : id, station_id, num_lights, status, has_flasher)
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

            



    # def __load_stations_from_file(self, file_name : str) -> None:
    #     """Load station settings from a config file"""
        
    #     # Counter for station init
    #     station_num = 0

    #     # In config file, each line represents a station,
    #     # each line (station) has a group of lights seperated by spaces,
    #     # each group is seperated by a '-' with left side representing
    #     # number of lights and right side representing the color.

    #     # Open config file
    #     file = open(file_name, 'r')

    #     for line in file:
    #         # TODO : Set up has_flasher for each station

    #         # Create a staton object
    #         new_station = self.__Station(station_num, 1, True, False)
    #         # Get next line; Split light groups seperated by whitespace
    #         station_info = line.strip().split(' ')
    #         # ID for each light position
    #         light_pos = 1
    #         for group in station_info:
                
    #             # Seperate num of lights and color for each group
    #             subgroup = group.split('-')
    #             num_color = int(subgroup[0])
    #             color = subgroup[1]
    #             # Init a light object and add it to station 
    #             for i in range(1, num_color + 1):
    #                 light = self.__Station.__Light(light_pos, station_num, color)
    #                 light_pos += 1
    #                 new_station.add_light(light)
    #         # Add station to station list
    #         self.stations.append(new_station)
    #         # increase station counter
    #         station_num += 1
            
    #     file.close()

    def get_light(self, station_id : int, light_pos : int):
        # Get station
        station = self.stations[station_id]

        # Get and return light
        return station.get_light(light_pos)

    def __str__(self):
        """Return string representation of object"""
        print("+++++++++ Stations ++++++++\n")
        for station in self.stations:
            print(station)
        
        print("\n+++++++++ Lights ++++++++\n")
        for station in self.stations:
            for light in station.lights:
                print(light)
        return ""
        

    