from textual.widgets import Label, Input, Button
from textual.containers import Vertical, Horizontal
from textual.widget import Widget
from textual.app import ComposeResult

class SideMenu(Widget):

    # TODO fix the nightmare that is on_compose() 

    def compose(self) -> ComposeResult:
        with Vertical():
            # Status Button
            with Horizontal(classes="line", id="status_line"):
                yield Button("Good", classes="sideb_wid", id="status")
            
            # Input Title
            with Horizontal(classes="line"):
                yield Label("Select Light", classes="sideb_wid", id="label")
            
            # Station input line
            with Horizontal(classes="line"):
                yield Label("Station:", classes="sideb_wid", id="in_station_label")
                yield Input(classes="sideb_wid", id="station_input", type="integer", max_length=2)
                yield Label(classes="in_spacer")
            
            # Light input line
            with Horizontal(classes="line"):       
                yield Label("Light:", classes="sideb_wid", id="in_light_label")
                yield Input(classes="sideb_wid", id="light_input", type="integer", max_length=2)
                yield Label(classes="in_spacer")
            with Horizontal(id="button_line"):
                yield Button("Select Light", id="light_select")
            with Horizontal(id="line"):
                yield Label(id="selected_light")