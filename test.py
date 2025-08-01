from light_field import LightField
from db_init import DatabaseInterface as DB

def main():
    als = LightField("databases/als.db")
    als.get_light_data(2, 2)
    print(als.get_light_data(11, 1))  # Example to get light data
    # (id, station_id, pos, type, color, status, loop)

if __name__ == "__main__":
    main() 