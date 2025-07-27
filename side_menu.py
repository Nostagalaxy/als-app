from textual.widgets import Label, Input, Button
from textual.containers import Vertical, Horizontal
from textual.widget import Widget
from textual.app import ComposeResult
from textual.reactive import reactive

class SideMenu(Widget):

    # TODO fix this nightmare
    # |   |   |   |   |   |
    # v   v   v   v   v   v

    status = reactive("Status")

    def compose(self) -> ComposeResult:
        with Vertical():
            # Status Button
            with Horizontal(classes="line", id="status_line"):
                yield Button(label=self.status, classes="sideb_wid", id="status")
            
            # Input Title
            with Horizontal(classes="line"):
                yield Label("Select Light", classes="sideb_wid", id="label")
            
            # Station input line
            with Horizontal(classes="line"):
                yield Label("Station:", classes="sideb_wid", id="in_station_label")
                yield Input(classes="sideb_wid", id="station_input", max_length=2)
                yield Label(classes="in_spacer")
            
            # Light input line
            with Horizontal(classes="line"):       
                yield Label("Light:", classes="sideb_wid", id="in_light_label")
                yield Input(classes="sideb_wid", id="light_input", max_length=2)
                yield Label(classes="in_spacer")
            with Horizontal(id="button_line"):
                yield Button("Select Light", id="light_select")
            with Horizontal(id="line"):
                yield Label(id="selected_light")

    async def on_mount(self) -> None:
        status_button = self.query_one("#status", Button)
        if status_button is not None:
            status_button.label = self.status
        else:
            self.log("Status button not found in SideMenu on_mount()")

    def watch_status(self, value: str) -> None:
        status_button = self.query_one("#status", Button)
        if status_button is not None:
            status_button.label = str(value)
