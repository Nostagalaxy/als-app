from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Button, Input, Static

from als_diagram import ALSFDiagram
from light_field import LightField
from side_menu import SideMenu
from light_menu import LightMenu

class MyApp(App):
    CSS_PATH = [
        "css/app_main.tcss",
        "css/side_menu.tcss"
    ]

    DB_FILE_PATH = "databases/als.db"

    def __init__(self):
        super().__init__()
        self.als = LightField(self.DB_FILE_PATH)

    def compose(self) -> ComposeResult:
        yield Header(True, name="A.D.A.M")
        yield ALSFDiagram(id='diagram')
        yield SideMenu(id='sidebar')
        yield Footer()

    def on_button_pressed(self, event : Button.Pressed):
        if event.button.id == "light_select":
            # Check inputs have data and data is correct
            if self.is_valid_input():
                light_data : dict = self.get_light_from_input()
                self.push_screen(LightMenu(light_data))
            else:
                self.log("Invalid input light selection")

    # TODO -> Move this function under the ALS class

    def get_light_from_input(self) -> dict:
        station = int(self.query_one("#station_input", Input).value)
        light = int(self.query_one("#light_input", Input).value)
        return self.als.get_light_data(station, light)

    def is_valid_input(self) -> bool:
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
        num_lights : int = self.als.get_station_data(station_input)['num_lights']
        self.log("Input is valid, number of lights: " + str(num_lights))

        # Check if light input number is within range
        if light_input < 0 or light_input > num_lights:
            return False
        
        # Returns True if all other statements are passed
        return True

if __name__ == "__main__":
    app = MyApp()
    app.run()