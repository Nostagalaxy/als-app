from light_field import LightField
from monitor import Monitor

def main():
    als = LightField("databases/als.db")
    monitor = Monitor(als, "ALSF")

if __name__ == "__main__":
    main() 