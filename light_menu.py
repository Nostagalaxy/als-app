from textual.screen import ModalScreen
from textual.containers import Grid, Vertical, Horizontal
from textual.app import ComposeResult
from textual.widgets import Button, DataTable, Static, Checkbox, Header, Footer, Input, Switch
from textual.message import Message

from rich.text import Text

from light_field import LightField

class LightMenu(ModalScreen):
    """Screen for data and settings for Light"""
    
    CSS_PATH = "css/light_menu.tcss"

    class StatusChanged(Message):
        def __init__(self, station_id : int, light_pos : int, updated_status : bool) -> None:
            super().__init__()
            self.station_id = station_id
            self.light_pos = light_pos
            self.updated_status = updated_status

    class Exit(Message):
        def __init__(self) -> None:
            super().__init__()

    def __init__(self, light_data : dict, name: str | None = None, id: str | None = None, classes: str | None = None) -> None:
        super().__init__(name, id, classes)
        self.light_data = light_data

    def compose(self) -> ComposeResult:
        yield Header(True, name="Light Menu")
        
        with Grid():
            with Vertical(id="info_panel", markup=True) as Info:
                Info.border_title = "Info"

                # TODO Handle exception if light_data is None or invalid

                # Station : #
                content = Text.from_markup("[b]Station[/b] : " + "[bold purple]" + str(self.light_data['station_id']) + "[/bold purple]")
                yield Static(content, classes="line")
                
                # Light : #
                content = Text.from_markup("[b]Light[/b]   : " + "[bold purple]" + str(self.light_data['pos']) + "[/bold purple]")
                yield Static(content, classes="line")
                
                # TODO
                content = Text.from_markup("[b]Type[/b]    : " + "[bold]" + str(self.light_data['type']) + "[/bold]")
                yield Static(content, classes="line")

                # Get color code and interpret into a string
                if self.light_data['color'] == 'green':
                    content = Text.from_markup("[b]Color[/b]   : " + "[bold green]Green[/bold green]")
                elif self.light_data['color'] == 'red':
                    content = Text.from_markup("[b]Color[/b]   : " + "[bold red]Red[/bold red]")
                elif self.light_data['color'] == 'white':
                    content = Text.from_markup("[b]Color[/b]   : " + "[bold white]White[/bold white]")
                else:
                    raise ValueError(f"Invalid color: {self.light_data['color']}")
                
                yield Static(content, classes="line")

                # TODO
                yield Static("Loop    :")
                yield Static("Address :")

                yield Button("Quit", id="quit")

            with Vertical(id='data_panel'):
                yield DataTable()
                yield Input()
                with Horizontal():
                    yield Button("Log", variant="primary", classes="data_button")
                    yield Button("Edit", classes="data_button")
                    yield Button("Delete", classes="data_button")

            with Vertical(name="Light Status", id="status_panel") as Status:
                Status.border_title = "Status"
                content = Text.from_markup("[bold red]OTS[/bold red]")
                yield Static(content,classes="leftside_line")
                yield Switch(value=self.light_data['status'])

                yield Checkbox("Light", id="lm_checkbox_light")
                yield Checkbox("Transciever")
            
        yield Footer()

    def on_button_pressed(self, event : Button.Pressed) -> None:
        if event.button.id == "quit":
            self.app.pop_screen()  

    def on_switch_changed(self, event : Switch.Changed) -> None:
        # Check if the status has changed
        if event.switch.value is not self.light_data['status']:
            
            # Update the status in the menu
            self.light_data['status'] = event.switch.value

            # Post message to update light field
            self.post_message(
                self.StatusChanged(
                    self.light_data['station_id'],                                  
                    self.light_data['pos'], 
                    event.switch.value))
            
