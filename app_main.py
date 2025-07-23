from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Button, Input, Static

from als_diagram import ALSFDiagram
from als import Als
from side_menu import SideMenu
from light_menu import LightMenu

class MyApp(App):
    CSS_PATH = [
        "css/app_main.tcss",
        "css/side_menu.tcss"
    ]

    def __init__(self):
        super().__init__()
        self.als = Als()

    def compose(self) -> ComposeResult:
        yield Header(True, name="A.D.A.M")
        yield ALSFDiagram(id='diagram')
        yield SideMenu(id='sidebar')
        yield Footer()

    def on_button_pressed(self, event : Button.Pressed):
        if event.button.id == "light_select":
            # Check inputs have data and data is correct
            if self.__is_valid_input():
                light : Als.Light = self.__get_light_from_input()
                self.push_screen(LightMenu(light))
            else:
                self.log("Invalid selection")

    # TODO -> Move this function under the ALS class

    def __get_light_from_input(self) -> Als.Light:
        station = int(self.query_one("#station_input", Input).value)
        light = int(self.query_one("#light_input", Input).value)
        return self.als.get_light(station, light)

    def __is_valid_input(self) -> bool:
        # Get data from inputs
        try:
            station_input = int(self.query_one("#station_input", Input).value)
            light_input = int(self.query_one("#light_input", Input).value)
        except ValueError:
            return False

        # Check if number is within range
        if station_input < 0 or station_input > 24:
            return False
        
        # Get station to determine number of lights
        station : Als.Station = self.als.stations[station_input]

        # Check if light input number is within range
        if light_input < 0 or light_input > station.size:
            return False
        
        # Returns True if all other statements are passed
        return True

if __name__ == "__main__":
    app = MyApp()
    app.run()