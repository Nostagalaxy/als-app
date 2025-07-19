import asyncio
from textual.containers import VerticalScroll, Horizontal, Widget
from textual.events import Click
from textual.widgets import Static
from textual.app import ComposeResult
from textual.message import Message
from textual.color import Color
from rich import print

from side_menu import SideMenu

class ALSFDiagram(Widget):
    #TODO create info on diagram once parent class is developed.

    # Different style lights
    UNICODE_GREEN : str = "\U0001F7E2"
    UNICODE_RED : str = "\U0001F534"
    UNICODE_WHITE : str = "\u26AA"
    ASCII_GREEN : str = "[bold green]O[/]"
    ASCII_RED : str = "[bold red]O[/]"
    ASCII_WHITE : str = "[bold white]O[/]"

    current_station = None

    class LightTile(Static):
        """ 
            Light Tile inherits the Static widget and represents
            a light in the light field diagram usng Unicode icons.
        """

        # Member Variables
        is_blinking : bool = False

        class Selected(Message):
            """ Message that has ID of light selected """
            def __init__(self, light_id : str):
                self.light_id : int = light_id
                super().__init__()

        def on_click(self, event: Click) -> None:

            self.log('Station: ' + str(self.query_ancestor(Horizontal)) + 'selected.')
            station = self.query_ancestor(Horizontal)
            if station:
                station.styles.background = Color.parse('yellow')
                self.log('yellow backgr')
            else:
                self.log("No Horizontal ancestor found.")
        
        # Blink when blink state is set to true
        async def blink(self) -> None:
            while self.is_blinking:
                self.add_class("blink")
                await asyncio.sleep(1.0)
                self.remove_class("blink")
                await asyncio.sleep(1.0)

    # DEBUG FUNCTION TO TRACK LIGHT ID MESSAGE ***
    def on_light_tile_selected(self, message : LightTile.Selected) -> None:
        self.app.log(f'Diagram got message : {message} from : {message.light_id}.')

    def on_click(self, event : Click):
        self.log(str(event.widget))         # DEBUG
        station_num : int = -1
        if(isinstance(event.widget, Horizontal) and (self.current_station is None)):
            station_num = event.widget.id
            self.current_station = station_num[1:]
            self.log('No current station')  # DEBUG
            self.log(station_num)           # DEBUG
        elif(event.widget, Horizontal):
            station_num = event.widget.id
            current_station = station_num[1:]
            self.log(station_num)           # DEBUG

    def compose(self):
        """ Composes all widgets of the Diagram"""
        
        # TODO
        # Add code to include flashers in 1000 >= outer stations

        with VerticalScroll():
            for s in range(0, 25):
                with Horizontal(classes="station", id="s" + str(s)):
                    # Threshold bar
                    if s == 0:
                        yield from self.generate_threshold(s)
                    
                    # 500' bar
                    elif s == 5:
                        yield from self.generate_500_foot(s)
                    
                    # 200' - 400' and 600' to 900' with red wing bars
                    elif ((s > 0 and s < 5) or (s < 10 and s > 5)):
                        yield from self.generate_inner_bars(s)
                    
                    # 1000' bar
                    elif(s == 10):
                        yield from self.generate_1000_foot(s)
                    
                    # 1100' - 2400' bars
                    else:
                        yield from self.generate_outer_bars(s)
    
    def generate_threshold(self, station_id: int) -> ComposeResult:
        for light_pos in range(1, 50):
    
            # Green threshold
            yield self.LightTile(self.ASCII_GREEN, classes="light", id='_' + str(station_id) + '-' + str(light_pos))

    def generate_500_foot(self, station_id: int) -> ComposeResult:
        for light_pos in range(1, 20):
    
            # Red wing bar light  
            if((light_pos > 0 and light_pos < 4) or (light_pos > 16 and light_pos < 20)):
                yield self.LightTile(self.ASCII_RED, classes="light", id='_' + str(station_id) + '-' + str(light_pos))
    
            # White center light
            else:
                yield self.LightTile(self.ASCII_WHITE, classes="light", id='_' + str(station_id) + '-' + str(light_pos))

    def generate_1000_foot(self, station_id : int) -> ComposeResult:
        light_pos = 1
        for light_pos in range(1, 24):
    
            # Spacer
            if(light_pos == 9 or light_pos == 15):
                yield Static(' ', classes='light')
    
            # White light
            else:
                yield self.LightTile(self.ASCII_WHITE, classes='light', id='-' + 's' + str(station_id) + '-light_pos' + str(light_pos))
                light_pos += 1
    
    def generate_inner_bars(self, station_id : int) -> ComposeResult:
        light_pos = 1
        for light_pos in range(1, 21):
    
            # Red wing bar light                
            if((light_pos >=1 and light_pos <= 3) or (light_pos >= 17 and light_pos <= 19)):
                yield self.LightTile(self.ASCII_RED, classes="light", id='-' + 's' + str(station_id) + '-light_pos' + str(light_pos))
                light_pos += 1        
    
            # Spacer
            elif((light_pos >= 4 and light_pos <= 7) or (light_pos >= 13 and light_pos <= 16)):
                yield Static(" ", classes='light')
    
            # White center light
            elif(light_pos >= 8 and light_pos <= 12):
                yield self.LightTile(self.ASCII_WHITE, classes="light", id='_' + str(station_id) + '-' + str(light_pos))  
                light_pos += 1

    def generate_outer_bars(self, station_id : int) -> ComposeResult:
        for light_pos in range(1, 6):
            yield self.LightTile(self.ASCII_WHITE, classes="light", id='_' + str(station_id) + '-' + str(light_pos))