from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Button

from als_diagram import ALSFDiagram
from side_menu import SideMenu
from light_menu import LightMenu

class MyApp(App):
    CSS_PATH = [
        "css/app_main.tcss",
        "css/side_menu.tcss"
    ]

    def compose(self) -> ComposeResult:
        yield Header(True, name="A.D.A.M")
        yield ALSFDiagram(id='diagram')
        yield SideMenu(id='sidebar')
        yield Footer()

    def on_button_pressed(self, event : Button.Pressed):
        if event.button.id == "light_select":
            self.push_screen(LightMenu())


if __name__ == "__main__":
    app = MyApp()
    app.run()