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
        
        def add_light_out(self, light: dict) -> None:
            """Add a light outage to the section."""
            if light not in self.lights_out:
                self.lights_out.append(light)
                self.lights_out.sort(key=lambda l: l['station_id'])

        def add_bar_out(self, station_id: int) -> None:
            """Add a station outage to the section."""
            if station_id not in self.bars_out:
                self.bars_out.append(station_id)
                self.bars_out.sort()

        def check_tolerances(self, rand_lights_out: int, adjacents: int, rand_light_tolerance: int, adjacent_tolerance: int) -> 'Monitor.State':
            """Check if the tolerances are exceeded."""
            if(rand_lights_out > rand_light_tolerance or adjacents > adjacent_tolerance):
                #DEBUG
                print(f"FAILURE : rand lights out = {rand_lights_out}, adjacents = {adjacents}")
                return Monitor.State.FAILURE
            elif(rand_lights_out == rand_light_tolerance or adjacents == adjacent_tolerance):
                #DEBUG
                print(f"ALERT : rand lights out = {rand_lights_out}, adjacents = {adjacents}")
                return Monitor.State.ALERT
            else:
                #DEBUG
                print(f"NORMAL : rand lights out = {rand_lights_out}, adjacents = {adjacents}")
                return Monitor.State.NORMAL

        def update_five_bars(self) -> None:
            """Update the bars out in the inner 1500 section."""
            # First check if there are any bars out and add to self.bars_out
            cur_bar: int = 1
            cur_lights_out: int = 0

            for light in self.lights_out:
                # If the station id matches the current station
                cur_id = light['station_id']
                
                # Check if the current bar is the same as the current light station id
                # If not, assign as current bar and reset current lights out
                if cur_bar != cur_id:
                    cur_bar = cur_id
                    cur_lights_out = 0
                
                # Increment current lights out
                cur_lights_out += 1

                if cur_lights_out > Monitor.Tolerances.FIVE_BAR_OUT:

                    # DEBUG
                    # if cur_lights_out >= 3: 
                    #     print(f"Bar out inner 1500 : {cur_id} @ {cur_lights_out}")

                    # Add bar to bars out if not already added
                    if cur_id not in self.bars_out:
                        self.bars_out.append(cur_id)
                        self.bars_out.sort()

        def update_three_bars(self, section_lights_out) -> None:
            """Update the bars out in the side rows section."""
            # First check if there are any bars out and add to self.bars_out
            cur_bar: int = 1
            cur_lights_out: int = 0

            for light in section_lights_out:
                # If the station id matches the current station
                cur_id = light['station_id']
                
                # Check if the current bar is the same as the current light station id
                # If not, assign as current bar and reset current lights out
                if cur_bar != cur_id:
                    cur_bar = cur_id
                    cur_lights_out = 0
                
                # Increment current lights out
                cur_lights_out += 1

                if cur_lights_out > Monitor.Tolerances.THREE_BAR_OUT:

                    # Add bar to bars out if not already added
                    if cur_id not in self.bars_out:
                        self.bars_out.append(cur_id)
                        self.bars_out.sort()

        def max_cons_bars(self, wing_bar: list | None) -> int:
            """Count the number of consecutive bars out."""
            count: int = 0
            previous_bar: int = 0
            
            # If wing_bar is None, use self.bars_out
            # Otherwise, use the wing_bar list
            if wing_bar is None:
                bars = self.bars_out
            else:
                # Extract station_id from each dict in the wing_bar list
                bars = [light['station_id'] for light in wing_bar if isinstance(light, dict) and 'station_id' in light]
                bars = sorted(list(set(bars)))

            # Loop through each bar
            for bar in bars:
                # If the current bar is the same as the previous bar or if there is no previous bar
                # Increment count if consecutive
                if bar - 1 == previous_bar or previous_bar == 0:
                    count += 1
                # If not consecutive, reset count
                else:
                    count = 0
                
                # Update previous bar
                previous_bar = bar
            
            return count

    class Threshold(Section):
        """Threshold section of the ALS system."""
        def __init__(self, status: 'Monitor.State') -> None:
            super().__init__(status)

        def check(self) -> 'Monitor.State':
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
            
            return self.check_tolerances(rand_lights_out, max_adj_out,
                Monitor.Tolerances.THRESHOLD_RAND_LIGHTS_OUT, Monitor.Tolerances.THRESHOLD_ADJ_LIGHTS_OUT)
                
    class Inner1500(Section):
        """Inner 1500 section of the ALS system."""
        def __init__(self, status: 'Monitor.State') -> None:
            super().__init__(status)
     
        def check(self) -> 'Monitor.State':
            """Check if the inner 1500 section is in an outage state."""
        
            # Get total random lights out
            rand_lights_out: int = len(self.lights_out)
            
            # Update the bars out
            self.update_five_bars()

            # Check if the number of consecutive bars out exceeds the tolerance
            max_cons_bars_out: int = self.max_cons_bars(None)

            return self.check_tolerances(rand_lights_out, max_cons_bars_out, 
                Monitor.Tolerances.CENTER_INNER_1500_RAND_LIGHT_OUT, Monitor.Tolerances.CENTER_INNER_1500_CONS_BAR_OUT)

    class Outer1500(Section):
        """Outer 1500 section of the ALS system."""
        def __init__(self, status: 'Monitor.State') -> None:
            super().__init__(status)
            rand_light_tolerance: Final = Monitor.Tolerances.CENTER_OUTER_1500_RAND_LIGHT_OUT
            cons_bar_tolerance: Final = Monitor.Tolerances.CENTER_OUTER_1500_CONS_BAR_OUT

        def check(self) -> 'Monitor.State':
            """Check if the outer 1500 section is in an outage state."""
            # Get total random lights out
            rand_lights_out: int = len(self.lights_out)
            
            # Update the bars out
            self.update_five_bars()

            # Check if the number of consecutive bars out exceeds the tolerance
            max_cons_bars: int = self.max_cons_bars(None)

            return self.check_tolerances(rand_lights_out, max_cons_bars,
                Monitor.Tolerances.CENTER_OUTER_1500_RAND_LIGHT_OUT, Monitor.Tolerances.CENTER_OUTER_1500_CONS_BAR_OUT)
        
    class SideRows(Section):
        """Side rows section of the ALS system."""
        def __init__(self, status: 'Monitor.State') -> None:
            super().__init__(status)

        def split(self) -> None:
            """Split the lights out into left and right wings."""
            # Split the lights out into left and right wings
            self.left_wing_lights_out = [light for light in self.lights_out if light['pos'] < 4]
            self.right_wing_lights_out = [light for light in self.lights_out if light['pos'] >= 9]

        def check(self) -> 'Monitor.State':
            """Check if the side rows section is in an outage state."""
            
            # Split the lights out into left and right wings
            self.split()

            # Get total random lights out
            rand_lights_out: int = len(self.lights_out)
            
            # Update the bars out
            self.update_three_bars(self.left_wing_lights_out)
            #DEBUG
            print(f"Left wing lights out: {self.left_wing_lights_out}")
            self.update_three_bars(self.right_wing_lights_out)
            #DEBUG
            print(f"Right wing lights out: {self.right_wing_lights_out}")

            # Check if the number of consecutive bars out exceeds the tolerance
            max_cons_bars: int = max(self.max_cons_bars(self.left_wing_lights_out), self.max_cons_bars(self.right_wing_lights_out))

            return self.check_tolerances(rand_lights_out, max_cons_bars,
                Monitor.Tolerances.SIDE_ROW_RAND_LIGHT_OUT, Monitor.Tolerances.SIDE_ROW_CONS_BAR_OUT)

    class FiveHundred(Section):
        """500' section of the ALS system."""
        def __init__(self, status: 'Monitor.State') -> None:
            super().__init__(status)

        def check(self) -> 'Monitor.State':
            """Check if the 500' section is in an outage state."""
            rand_lights_out: int = len(self.lights_out)
            return self.check_tolerances(rand_lights_out, 0,
                Monitor.Tolerances.FIVE_HUND_LIGHTS_OUT, 255) # No adjacent lights out tolerance
        
    class OneThousand(Section):
        """1000' section of the ALS system."""
        def __init__(self, status: 'Monitor.State') -> None:
            super().__init__(status)

        def check(self) -> 'Monitor.State':
            """Check if the 1000' section is in an outage state."""
            rand_lights_out: int = len(self.lights_out)
            return self.check_tolerances(rand_lights_out, 0,
                Monitor.Tolerances.ONE_THOUS_LIGHTS_OUT, 255) # No adjacent lights out tolerance

    #Flashers section
    # TODO -> Implement flashers section

    def __init__(self, light_field : LightField, type : str) -> None:
        self.als : LightField = light_field
        
        self.status: Monitor.State = Monitor.State.NORMAL

        self.num_alerts: int = 0
        self.num_failures: int = 0

        self.inner_1500 = Monitor.Inner1500(Monitor.State.NORMAL)
        self.outer_1500 = Monitor.Outer1500(Monitor.State.NORMAL)
        self.side_rows = Monitor.SideRows(Monitor.State.NORMAL)
        self.threshold = Monitor.Threshold(Monitor.State.NORMAL)
        self.five_hundred = Monitor.FiveHundred(Monitor.State.NORMAL)
        self.one_thousand = Monitor.OneThousand(Monitor.State.NORMAL)
        #self.flashers = Monitor.Section(Monitor.State.NORMAL)           #TODO

        # TODO --> THis might not work
        self.sections = {
            self.inner_1500,
            self.outer_1500,
            self.side_rows,
            self.threshold,
            self.five_hundred,
            self.one_thousand
            #self.flashers
        }

        self.update()

    def update(self) -> None:
        # Data is (station_id, pos)
        # Get a fresh list of lights out everytime you need to update
        lights_out = self.als.get_lights_out()
        
        # Loop through each light out
        for light in lights_out:
            # Add light to the appropriate section
            # Threshold section
            if light["station_id"] == 0:
                self.threshold.add_light_out(light)
            # 500' section
            elif light["station_id"] == 5:
                self.five_hundred.add_light_out(light)
            # 1000' section
            elif light["station_id"] == 10:
                self.one_thousand.add_light_out(light)
            # Outer 1500 section
            elif light["station_id"] > 15:
                self.outer_1500.add_light_out(light)
            # Row bar sections
            elif (light["pos"] > 0 and light["pos"]) < 4 or (light["pos"] > 8 and light["pos"] < 12):
                self.side_rows.add_light_out(light)
            # Inner 1500 section
            elif light["pos"] > 3 and light["pos"] < 9:
                self.inner_1500.add_light_out(light)
            
        self.status = self.check()

    def check(self) -> 'Monitor.State':
        """Check the system status."""

        for section in self.sections:
            # Check if the section is in an outage state
            section.status = section.check()
            
            temp_status = Monitor.State.NORMAL

            if section.status == Monitor.State.FAILURE:
                # If any section is in a failure state, the system is in a failure state
                temp_status = Monitor.State.FAILURE
                self.num_failures += 1
            elif section.status == Monitor.State.ALERT and temp_status != Monitor.State.FAILURE:
                # If any section is in an alert state, the system is in an alert state
                temp_status = Monitor.State.ALERT
                self.num_alerts += 1
        
        return temp_status
    
    def get_status(self) -> 'Monitor.State':
        """Get the current system status."""
        
        #DEBUG
        print(f"Number of alerts : {self.num_alerts},\nNumber of failures : {self.num_failures}")

        return self.status
    
    def get_num_alerts(self) -> int:
        """Get the number of alerts."""
        return self.num_alerts
    
    def get_num_failures(self) -> int:
        """Get the number of failures."""
        return self.num_failures