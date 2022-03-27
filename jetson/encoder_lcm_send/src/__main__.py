import time
import random
import asyncio
from rover_common import aiolcm
from rover_msgs import DriveVelData

def send_encoders(lcm, vel):
    for i in range(6):
        msg = DriveVelData()
        msg.axis = i
        msg.vel_percent = vel
        msg.current_amps = 1
        lcm.publish("/drive_vel_data", msg.encode()) 
    
def main():
    lcm = aiolcm.AsyncLCM()

    tic = time.perf_counter()
    while(time.perf_counter() - tic < 10):
        send_encoders(lcm, 0) 
        time.sleep(1)

    tic = time.perf_counter()
    while(time.perf_counter() - tic < 10):
        send_encoders(lcm, 10) 
        time.sleep(1)

    tic = time.perf_counter()
    while(time.perf_counter() - tic < 10):
        send_encoders(lcm, 0) 
        time.sleep(1)

    tic = time.perf_counter()
    while(time.perf_counter() - tic < 10):
        send_encoders(lcm, 10) 
        time.sleep(1)

if __name__ == "__main__":
    main()
