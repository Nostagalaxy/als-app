from light_field import LightField

def main():
    DB_FILE = "databases/als.db"

    als = LightField(DB_FILE)
    print(als)

if __name__ == "__main__":
    main() 