from als import Als
from db_init import DatabaseInterface as DB

def main():
    db = DB("databases/als.db")
    db.get_all_stations()
    db.commit()

if __name__ == "__main__":
    main() 