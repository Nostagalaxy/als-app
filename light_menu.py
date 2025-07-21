from textual.screen import Screen
from textual.containers import Grid, Vertical
from textual.app import ComposeResult
from textual.widgets import Button, DataTable, Static, RadioButton, RadioSet

from als import Als

class LightMenu(Screen):
    """Screen for data and settings for Light"""
    
    CSS_PATH = "css/light_menu.tcss"

    def __init__(self, light : Als.Light, name: str | None = None, id: str | None = None, classes: str | None = None) -> None:
        super().__init__(name, id, classes)
        self.light = light


    def compose(self) -> ComposeResult:

        with Grid():
            with Vertical(id="left_panel"):
                yield Static("Station : " + str(self.light.station_id))
                yield Static('Light : ' + str(self.light.pos))
                yield Static("OTS")
                with RadioSet():
                    yield RadioButton("Light")
                    yield RadioButton("Transciever")
                yield Button("Quit", id="quit")
            with Vertical(id='right_panel'):
                yield DataTable()

    def on_button_pressed(self, event : Button.Pressed) -> None:
        if event.button.id == "quit":
            self.app.pop_screen()  

    def on_radio_button_changed(self, event : RadioButton.Changed) -> None:
        if event.radio_button:
            self.log("Button Changed") 
