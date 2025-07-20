from textual.containers import Widget
from textual.widgets import Static
from rich import print

from als import Als

def main():
    als = Als()
    print(als.get_light(22, 4))

if __name__ == "__main__":
    main() 