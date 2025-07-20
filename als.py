from enum import Enum

class Als:

    class Status(Enum):
        INS = 1
        OTS = 2

    class Light:
        def __init__(self, pos : int, color : str):
            self.pos = pos
            self.color = color

    class Station:
        lights = []

        def __init__(self, id : int, has_flasher : bool):
            self.id = id
            self.has_flasher = has_flasher

        def add_light(self, light) -> None:
            self.lights.append(light) 

    def __init__(self):
        self.stations = []
        self.__load_stations_from_file('als_config.txt')
        
        

    def __load_stations_from_file(self, file_name : str) -> list:
        # Counter for station init
        station_num = 0

        # In config file, each line represents a station,
        # each line (station) has a group of lights seperated by spaces,
        # each group is seperated by a '-' with left side representing
        # number of lights and right side representing the color.

        # Open config file
        file = open(file_name, 'r')

        for line in file:
            # Create a staton object
            # TODO : Set up has_flasher for each station
            new_station = self.Station(station_num, False)
            # Get next line; Split light groups seperated by whitespace
            station_info = line.strip().split(' ')
            for group in station_info:
                # Seperate num of lights and color for each group
                subgroup = group.split('-')
                num_lights = int(subgroup[0])
                color = subgroup[1]
                # Init a light object and add it to station 
                for i in range(1, num_lights + 1):
                    light = self.Light(i, color)
                    new_station.add_light(light)
            # Add station to station list
            self.stations.append(new_station)
            # increase station counter
            station_num += 1
            
        file.close()

    def get_Light(station_id : int, light_pos : int) -> Light:
        pass

    