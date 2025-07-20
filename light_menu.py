from textual.screen import Screen
from textual.containers import Grid
from textual.app import ComposeResult
from textual.widgets import Label, Button

class LightMenu(Screen):
    """Screen for data and settings for Light"""
    
    CSS_PATH = "css/light_menu.tcss"

    def compose(self) -> ComposeResult:
        yield Button("Quit", id="quit")

    def on_button_pressed(self, event : Button.Pressed) -> None:
        if event.button.id == "quit":
            self.app.pop_screen()   
