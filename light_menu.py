from textual.screen import Screen
from textual.containers import Grid, Vertical
from textual.app import ComposeResult
from textual.widgets import Button, Static, RadioButton

from als import Als

class LightMenu(Screen):
    """Screen for data and settings for Light"""
    
    CSS_PATH = "css/light_menu.tcss"

    def __init__(self, light : Als._Light, name: str | None = None, id: str | None = None, classes: str | None = None) -> None:
        super().__init__(name, id, classes)
        self.light = light


    def compose(self) -> ComposeResult:

        with Grid():
            with Vertical(id="left_panel"):
                yield Static("Station : " + str(self.light.station_id))
                yield Static('Light : ' + str(self.light.pos))
                yield Static("OTS")
                yield RadioButton("Light")
                yield RadioButton("Transciever")
                yield Button("Quit", id="quit")
            with Vertical(id='right_panel'):
                yield Static('Right Side')

    def on_button_pressed(self, event : Button.Pressed) -> None:
        if event.button.id == "quit":
            self.app.pop_screen()   
