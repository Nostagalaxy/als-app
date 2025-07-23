from light_field import LightField

def main():
    DB_FILE = "databases/als.db"

    als = LightField(DB_FILE)
    print(als)

    # (id, station_id, pos, type, color, status, loop)

if __name__ == "__main__":
    main() 