from typing import Final
from light_field import LightField

class Monitor():
    """Monitor class to track outages and system status."""

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

    def __init__(self, light_field : LightField, type : str) -> None:
        self.als : LightField = light_field
        self.lights_out: tuple = []
        self.overall_status: str = "Normal"
        self.inner_1500_status: bool = True
        self.outer_1500_status: bool = True
        self.side_row_status: bool = True
        self.threshold_status: bool = True
        self.five_hundred_status: bool = True
        self.one_thousand_status: bool = True
        self.flashes_status: bool = True

        self.lights_out = self.als.get_lights_out()

        self.update()

    def update(self) -> None:
        pass

    