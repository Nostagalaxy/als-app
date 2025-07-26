import asyncio
from textual.containers import VerticalScroll, Horizontal, Container
from textual.events import Click
from textual.widget import Widget
from textual.widgets import Static
from textual.app import ComposeResult
from textual.message import Message
from rich import print

class ALSFDiagram(Container):
    
    #                       TODO 
    # create info on diagram once parent class is developed.
    # Fix LightTile on_click() where click event is a Static or LightTile

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

        def __init__(self, content = "", *, expand = False, shrink = False, markup = True, name = None, id = None, classes = None, disabled = False):
            super().__init__(content, expand=expand, shrink=shrink, markup=markup, name=name, id=id, classes=classes, disabled=disabled)
            self.is_blinking : bool = False

        class Selected(Message):
            """ Message that has ID of light selected """
            def __init__(self, light_id : int):
                self.light_id : int = light_id
                super().__init__()

        def on_click(self, event: Click) -> None:
            if event.widget is not None:
                self.log(str(event.widget.id))
            else:
                self.log("Widget is none!")
        
        # Blink when blink state is set to true
        async def blink(self) -> None:
            while self.is_blinking:
                self.add_class("blink")
                await asyncio.sleep(1.0)
                self.remove_class("blink")
                await asyncio.sleep(1.0)

    def __init__(self, *children: Widget, name: str | None = None, id: str | None = None, classes: str | None = None, disabled: bool = False, markup: bool = True) -> None:
        super().__init__(*children, name=name, id=id, classes=classes, disabled=disabled, markup=markup)
        self.previous_station : Horizontal | None = None
        self.current_station : Horizontal | None = None


    def on_click(self, event : Click):
        """ Highlights station when diagram is clicked """

        # Update current station
        if event.widget is None:
            pass
        # If event is a Horizontal 
        elif isinstance(event.widget, Horizontal):
            
            self.current_station = event.widget
        # If event is a LightTile
        else:
            # Get the Horizontal parent of LightTile
            self.current_station = event.widget.query_ancestor(Horizontal)

        # Check if a previous station is highlighted
        if self.previous_station is not None:
            # Un-highlight that station
            self.previous_station.styles.background = 'yellow 0%'
        
        # Highlight selected station if available
        if self.current_station is not None:
            self.current_station.styles.background = 'yellow 20%'

        # Set previous station to current station
        self.previous_station = self.current_station

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
        for l in range(1, 24):
    
            # Spacer
            if(l == 9 or l == 15):
                yield Static(' ', classes='light')
    
            # White light
            else:
                yield self.LightTile(self.ASCII_WHITE, classes='light', id='_' + str(station_id) + '-' +  str(light_pos))
                light_pos += 1
    
    def generate_inner_bars(self, station_id : int) -> ComposeResult:
        light_pos = 1
        for l in range(1, 21):
    
            # Red wing bar light                
            if((l >=1 and l <= 3) or (l >= 17 and l <= 19)):
                yield self.LightTile(self.ASCII_RED, classes="light", id='_' + str(station_id) + '-' + str(light_pos))
                light_pos += 1        
    
            # Spacer
            elif((l >= 4 and l <= 7) or (l >= 13 and l <= 16)):
                yield Static(" ", classes='light')
    
            # White center light
            elif(l >= 8 and l <= 12):
                yield self.LightTile(self.ASCII_WHITE, classes="light", id='_' + str(station_id) + '-' + str(light_pos))  
                light_pos += 1

    def generate_outer_bars(self, station_id : int) -> ComposeResult:
        for light_pos in range(1, 6):
            yield self.LightTile(self.ASCII_WHITE, classes="light", id='_' + str(station_id) + '-' + str(light_pos))