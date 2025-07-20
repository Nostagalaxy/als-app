from textual.screen import Screen
from textual.containers import Grid
from textual.app import ComposeResult
from textual.widgets import Label, Button

class LightMenu(Screen):
    """Screen for data and settings for Light"""
    
    def on_compose(self) -> ComposeResult:
        yield Grid(
            Label("Hello"),
            Button("Quit", classes="light_menu", id="quit")
        )

    def on_button_pressed(self, event : Button.Pressed) -> None:
        if event.button.id == "quit":
            self.app.pop_screen()   
