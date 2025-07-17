import asyncio
from textual.containers import VerticalScroll, Horizontal, Widget
from textual.events import Click
from textual.widgets import Static
from textual.app import ComposeResult
from textual.message import Message
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
            
            self.app.log(f'{self.id} selected.')                                           #  DEBUG
            
            # Send event of light id when clicked
            self.post_message(self.Selected(self.id))

            # Set blink state when clicked on
            self.is_blinking = not self.is_blinking
            self.run_worker(self.blink())
        
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
        for l in range(1, 50):
    
            # Green threshold
            yield self.LightTile(self.ASCII_GREEN, classes="light", id='s' + str(station_id) + '-l' + str(l))

    def generate_500_foot(self, station_id: int) -> ComposeResult:
        for l in range(1, 20):
    
            # Red wing bar light  
            if((l > 0 and l < 4) or (l > 16 and l < 20)):
                yield self.LightTile(self.ASCII_RED, classes="light", id='s' + str(station_id) + '-l' + str(l))
    
            # White center light
            else:
                yield self.LightTile(self.ASCII_WHITE, classes="light", id='s' + str(station_id) + '-l' + str(l))

    def generate_1000_foot(self, station_id : int) -> ComposeResult:
        light_pos = 1
        for l in range(1, 24):
    
            # Spacer
            if(l == 9 or l == 15):
                yield Static(' ', classes='light')
    
            # White light
            else:
                yield self.LightTile(self.ASCII_WHITE, classes='light', id='s' + str(station_id) + '-l' + str(light_pos))
                light_pos += 1
    
    def generate_inner_bars(self, station_id : int) -> ComposeResult:
        light_pos = 1
        for l in range(1, 21):
    
            # Red wing bar light                
            if((l >=1 and l <= 3) or (l >= 17 and l <= 19)):
                yield self.LightTile(self.ASCII_RED, classes="light", id='s' + str(station_id) + '-l' + str(light_pos))
                light_pos += 1        
    
            # Spacer
            elif((l >= 4 and l <= 7) or (l >= 13 and l <= 16)):
                yield Static(" ", classes='light')
    
            # White center light
            elif(l >= 8 and l <= 12):
                yield self.LightTile(self.ASCII_WHITE, classes="light", id='s' + str(station_id) + '-l' + str(light_pos))  
                light_pos += 1

    def generate_outer_bars(self, station_id : int) -> ComposeResult:
        for l in range(1, 6):
            yield self.LightTile(self.ASCII_WHITE, classes="light", id='s' + str(station_id) + '-l' + str(l))