from enum import Enum

class Als:

    class Status(Enum):
        INS = 1
        OTS = 2

    class Light:
        def __init__(self, pos, color):
            self.pos = pos
            self.color = color

    class Station:
        lights = []

        def add_light(self, light):
            self.lights.append(light) 

    def __init__(self):
        # Make comments to make this make sense
        self.lights = []
        self.stations = []

        file = open('als_config.txt', 'r')
        station_num = 0
        
        for line in file:
            new_station = self.Station()
            station_info = line.strip().split(' ')
            for group in station_info:
                subgroup = group.split('-')
                num_lights = int(subgroup[0])
                color = subgroup[1]
                for i in range(1, num_lights + 1):
                    light = self.Light(i, color)
                    new_station.add_light(light)

            self.stations.append(new_station)
            print(new_station)
            
        file.close()

    def get_Light(station_id : int, light_pos : int) -> Light:
        pass

    