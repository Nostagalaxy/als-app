from textual.app import App, ComposeResult
from textual.containers import Vertical, Horizontal, Container, VerticalScroll
from textual.widgets import RadioButton, Static, Header, Label
from textual.message import Message
from textual.events import Click

from als_diagram import ALSFDiagram
from side_menu import SideMenu

class MyApp(App):
    CSS_PATH = [
        "css/app_main.tcss",
        "css/side_menu.tcss"
    ]

    def compose(self) -> ComposeResult:
        yield ALSFDiagram(id='diagram')
        yield SideMenu(id='sidebar')

        print('App widgets composed!') # DEBUG


if __name__ == "__main__":
    app = MyApp()
    app.run()