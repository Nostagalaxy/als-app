from enum import Enum
from rich import print

class Als:

    #                                   TODO  
    #       - Set up has_flasher for each station in __load_stations_from_file()
    #       - Create multiple config files for different systems 

    CONFIG_FILE = "als_config.txt"

    class _Status(Enum):
        INS = 1
        OTS = 2

    class _Light:
        def __init__(self, pos : int, station_id : int, color : str) -> None:
            self.pos = pos
            self.color = color
            self.station_id = station_id

        def __str__(self):
            return f"[*Light* Station : {self.station_id}, Pos : {self.pos}, Color : {self.color}]"

    class _Station:

        def __init__(self, id : int, has_flasher : bool) -> None:
            self.id = id
            self.has_flasher = has_flasher
            self.lights = []
            self.size : int = 0

        def add_light(self, light) -> None:
            """Add light to station"""
            self.lights.append(light)
            self.size += 1 

        def get_light(self, pos : int):
            """Get light from indicated position"""
            return self.lights[pos - 1]

        def __str__(self):
            """Return s tring representation of object"""
            return f"[*Station* ID : {self.id}, Flasher : {self.has_flasher}]"

    def __init__(self) -> None:
        self.stations = []
        self.__load_stations_from_file(self.CONFIG_FILE)

    def __load_stations_from_file(self, file_name : str) -> list:
        """Load station settings from a config file"""
        
        # Counter for station init
        station_num = 0

        # In config file, each line represents a station,
        # each line (station) has a group of lights seperated by spaces,
        # each group is seperated by a '-' with left side representing
        # number of lights and right side representing the color.

        # Open config file
        file = open(file_name, 'r')

        for line in file:
            # TODO : Set up has_flasher for each station

            # Create a staton object
            new_station = self._Station(station_num, False)
            # Get next line; Split light groups seperated by whitespace
            station_info = line.strip().split(' ')
            # ID for each light position
            light_pos = 1
            for group in station_info:
                
                # Seperate num of lights and color for each group
                subgroup = group.split('-')
                num_color = int(subgroup[0])
                color = subgroup[1]
                # Init a light object and add it to station 
                for i in range(1, num_color + 1):
                    light = self._Light(light_pos, station_num, color)
                    light_pos += 1
                    new_station.add_light(light)
            # Add station to station list
            self.stations.append(new_station)
            # increase station counter
            station_num += 1
            
        file.close()

    def get_light(self, station_id : int, light_pos : int):
        # Get station
        station = self.stations[station_id]

        # Get and return light
        return station.get_light(light_pos)

    def __str__(self):
        print("+++++++++ Stations ++++++++\n")
        for station in self.stations:
            print(station)
        
        print("\n+++++++++ Lights ++++++++\n")
        for station in self.stations:
            for light in station.lights:
                print(light)
            print()

        return ""
        

    