from textual.containers import Widget
from textual.widgets import Static

class Test(Widget):
    
    def compose(self):
        yield Static("Hello!", id="word")
        