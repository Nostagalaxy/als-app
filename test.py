from textual.containers import Widget
from textual.widgets import Static
from rich import print

from als import Als
from db_init import DatabaseInterface as DB

def main():
    db = DB("databases/als.db")

    for i in range(11, 25):
        for j in range(1, 6):
            db.query("INSERT INTO lights (station_id, position, type, color, status) VALUES (?, ?, ?, ?, ?)", (i, j, "sb", "white", True))
                
                


    db.commit()


if __name__ == "__main__":
    main() 