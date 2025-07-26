from enum import Enum
from typing import Final
from light_field import LightField

class Monitor():
    """Monitor class to track outages and system status."""

    class Tolerances:
        #  *** System tolerances for ALSF ***
        # These numbers give the number of lights that can be out 
        # before the system is considered to be in an outage state.
        
        # Bar tolerances
        THREE_BAR_OUT: Final = 1
        FIVE_BAR_OUT: Final = 2

        CENTER_INNER_1500_CONS_BAR_OUT: Final = 2
        CENTER_INNER_1500_RAND_LIGHT_OUT: Final = 14
        # For 2400' configurations
        CENTER_OUTER_1500_CONS_BAR_OUT: Final = 2
        CENTER_OUTER_1500_RAND_LIGHT_OUT: Final = 8

        SIDE_ROW_CONS_BAR_OUT: Final = 2
        SIDE_ROW_RAND_LIGHT_OUT: Final = 9

        # For standard thresholds (49 lights)
        THRESHOLD_ADJ_LIGHTS_OUT: Final = 3
        THRESHOLD_RAND_LIGHTS_OUT: Final = 9

        FIVE_HUND_LIGHTS_OUT: Final = 3

        ONE_THOUS_LIGHTS_OUT: Final = 3

        FLASHERS_OUT: Final = 2

        TOTAL_LIGHTS_FLASHERS_OUT: Final = 27

    class State(Enum):
        """State of the ALS system."""
        NORMAL = "Normal"
        ALERT = "Outage"
        FAILURE = "Failure"

    class Section:
        """Section of the ALS system."""
        def __init__(self, status : 'Monitor.State') -> None:
            self.status: 'Monitor.State' = status
            self.bars_out: list = []
            self.lights_out: list = []
        
        def add_light_out(self, light : tuple) -> None:
            """Add a light outage to the section."""
            pass

        def add_bar_out(self, station_id: int) -> None:
            """Add a station outage to the section."""
            if station_id not in self.stations_out:
                self.stations_out.append(station_id)

    class Threshold(Section):
        """Threshold section of the ALS system."""
        def __init__(self, status: 'Monitor.State') -> None:
            super().__init__(status)

        def add_light_out(self, light: tuple) -> None:
            """Add a light outage to the threshold section."""
            if light not in self.lights_out:
                self.lights_out.append(light)

        def check_threshold(self) -> 'Monitor.State':
            """Check if the threshold is in an outage state."""
            # Random lights out
            rand_lights_out: int = len(self.lights_out)
            
            max_adj_out: int = 0
            count_adj_out: int = 0
            previous_pos: int = 0


            # Loop through each light out
            for light in self.lights_out:
                # If he current light is adjacent to the previous one check if zero to inculde into adjacent count
                if light['pos'] - 1 == previous_pos:
                    # Increment count of adjacent lights out
                    count_adj_out += 1

                    # Check if the count exceeds the maximum
                    if count_adj_out > max_adj_out:
                        max_adj_out = count_adj_out
                else:
                    # Reset count of adjacent lights out if not adjacent
                    count_adj_out = 0
                
                # Update previous position
                previous_pos = light['pos']

            # DEBUG                        
            print(f"Random tolerance exceeded :  {rand_lights_out > Monitor.Tolerances.THRESHOLD_RAND_LIGHTS_OUT} @ {rand_lights_out}\nAdjacent tolerance exceeded : {max_adj_out > Monitor.Tolerances.THRESHOLD_ADJ_LIGHTS_OUT} @ {max_adj_out}")
            
            if(rand_lights_out > Monitor.Tolerances.THRESHOLD_RAND_LIGHTS_OUT 
                or max_adj_out > Monitor.Tolerances.THRESHOLD_ADJ_LIGHTS_OUT):
                #DEBUG
                print("FAILURE")
                return Monitor.State.FAILURE
            elif(rand_lights_out == Monitor.Tolerances.THRESHOLD_RAND_LIGHTS_OUT 
                or max_adj_out == Monitor.Tolerances.THRESHOLD_ADJ_LIGHTS_OUT):
                #DEBUG
                print("ALERT")
                return Monitor.State.ALERT
            else:
                #DEBUG
                print("NORMAL")
                return Monitor.State.NORMAL
                


    def __init__(self, light_field : LightField, type : str) -> None:
        self.als : LightField = light_field
        
        self.system_status: Monitor.State = Monitor.State.NORMAL

        self.inner_1500 = Monitor.Section(Monitor.State.NORMAL)
        self.outer_1500 = Monitor.Section(Monitor.State.NORMAL)
        self.side_rows = Monitor.Section(Monitor.State.NORMAL)
        self.threshold = Monitor.Threshold(Monitor.State.NORMAL)
        self.five_hundred = Monitor.Section(Monitor.State.NORMAL)
        self.one_thousand = Monitor.Section(Monitor.State.NORMAL)
        self.flashers = Monitor.Section(Monitor.State.NORMAL)

        self.update()

    def update(self) -> None:
        # Data is (station_id, pos)
        # Get a fresh lists of lights out everytime you need to update

        lights_out = self.als.get_lights_out()
        # Loop through each light out
        for light in lights_out:
            # Check threshold lights
            if light["station_id"] == 0:
                self.threshold.add_light_out(light)

        self.threshold.check_threshold()

    