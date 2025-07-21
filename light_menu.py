from textual.screen import Screen
from textual.containers import Grid, Vertical, Horizontal
from textual.app import ComposeResult
from textual.widgets import Button, DataTable, Static, Checkbox, Header, Footer, Input

from rich.panel import Panel
from rich.text import Text

from als import Als

class LightMenu(Screen):
    """Screen for data and settings for Light"""
    
    CSS_PATH = "css/light_menu.tcss"

    def __init__(self, light : Als.Light, name: str | None = None, id: str | None = None, classes: str | None = None) -> None:
        super().__init__(name, id, classes)
        self.light = light


    def compose(self) -> ComposeResult:
        yield Header(True, name="Light Menu")
        
        with Grid():
            with Vertical(id="info_panel", markup=True) as Info:
                Info.border_title = "Info"

                # Station : #
                content = Text.from_markup("[b]Station[/b] : " + "[bold purple]" + str(self.light.station_id) + "[/bold purple]")
                yield Static(content, classes="line")
                
                # Light : #
                content = Text.from_markup("[b]Light[/b]   : " + "[bold purple]" + str(self.light.pos) + "[/bold purple]")
                yield Static(content, classes="line")
                
                # TODO
                yield Static("Type    : ")

                # Get color code and interpret into a string
                if self.light.color == 'g':
                    content = Text.from_markup("[b]Color[/b]   : " + "[bold green]Green[/bold green]")
                elif self.light.color == 'r':
                    content = Text.from_markup("[b]Color[/b]   : " + "[bold red]Red[/bold red]")
                elif self.light.color == 'w':
                    content = Text.from_markup("[b]Color[/b]   : " + "[bold white]White[/bold white]")
                
                yield Static(content, classes="line")

                # TODO
                yield Static("Loop    :")
                yield Static("Address :")



                yield Button("Quit", id="quit")

            with Vertical(id='data_panel'):
                yield DataTable()
                yield Input()
                with Horizontal():
                    yield Button("Log")
                    yield Button("Edit")
                    yield Button("Delete")

            with Vertical(name="Light Status", id="status_panel") as Status:
                Status.border_title = "Status"
                content = Text.from_markup("[bold red]OTS[/bold red]")
                yield Static(content,classes="leftside_line")
                
                yield Checkbox("Light", id="lm_checkbox_light")
                yield Checkbox("Transciever")
            
            
        
        yield Footer()

    def on_button_pressed(self, event : Button.Pressed) -> None:
        if event.button.id == "quit":
            self.app.pop_screen()  

    def on_checkbox_changed(self, event : Checkbox.Changed) -> None:
        if event.checkbox:
            self.log("Checkbox Changed") 
