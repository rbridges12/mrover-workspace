import time
import random
import asyncio
from rover_common import aiolcm
from rover_msgs import GPS

def random_gps():
    gps = GPS()
    gps.quality = 6
    gps.latitude_deg = 10
    gps.latitude_min = random.random() * 20
    gps.longitude_deg = 5
    gps.longitude_min = random.random() * 20
    return gps.encode()

def main():
    lcm = aiolcm.AsyncLCM()

    while True:
        lcm.publish("/gps", random_gps()) 
        time.sleep(0.1)


if __name__ == "__main__":
    main()
