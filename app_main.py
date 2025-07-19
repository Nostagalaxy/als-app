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

    def decode_id(self, in_id : str) -> dict:
        id_list : list[str] = in_id.split('-')
        
        light_str : str = id_list.pop()
        light_str = light_str[1]
        station_str : str = id_list.pop()
        station_str = station_str[1]

        light : int = int(light_str)
        station : int = int(station_str)

        decoded_id : dict = {station: light}

        return decoded_id


if __name__ == "__main__":
    app = MyApp()
    app.run()