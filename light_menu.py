from textual.screen import Screen
from textual.containers import Grid, Vertical
from textual.app import ComposeResult
from textual.widgets import Button, Static, RadioButton

class LightMenu(Screen):
    """Screen for data and settings for Light"""
    
    CSS_PATH = "css/light_menu.tcss"

    def compose(self) -> ComposeResult:
        with Grid():
            with Vertical(id="left_panel"):
                yield Static("Station #")
                yield Static('Light #')
                yield Static("OTS")
                yield RadioButton("Light")
                yield RadioButton("Transciever")
                yield Button("Quit", id="quit")
            with Vertical(id='right_panel'):
                yield Static('Right Side')


    def on_button_pressed(self, event : Button.Pressed) -> None:
        if event.button.id == "quit":
            self.app.pop_screen()   
