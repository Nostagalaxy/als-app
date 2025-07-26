from light_field import LightField
from monitor import Monitor

def main():
    als = LightField("databases/als.db")
    monitor = Monitor(als, "ALSF")
    print('Program completed successfully.')

if __name__ == "__main__":
    main() 