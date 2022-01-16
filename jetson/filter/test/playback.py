from os import path
from rover_msgs import IMUData, GPS
import json
import time
from datetime import datetime
from queue import Queue
import threading


IMU_DATA_SIZE = 13
GPS_DATA_SIZE = 7


def read_into_queue(file_path, data_type):
    queue = Queue()
    first_iter = False
    with open(file_path, "r") as f:
        while True:
            timestamp = f.readline()
            if not timestamp:
                break
            if not first_iter:
                first_iter = True
                first_timestamp = datetime.strptime(timestamp, "----- %Y-%m-%d %H:%M:%S.%f\n").timestamp() * 1000000
            json_string = ""
            for _ in range(IMU_DATA_SIZE if data_type == "imu" else GPS_DATA_SIZE):
                json_string += f.readline()
            f.readline()
            json_string = json_string.replace("\n", "").replace("\'", "\"")
            json_obj = json.loads(json_string)

            lcm = IMUData() if data_type == "imu" else GPS()
            for key, val in json_obj.items():
                setattr(lcm, key, val)
            queue.put(lcm)
    return queue, first_timestamp


"""
Opens specified test file then processes data into queues

Test files must be named: NAME_imu.txt and NAME_gps.txt

imu/gps_data are Queues of their respective LCM objects
first_imu/gps_timestamp are the timestamp of the first recorded LCM data in microseconds
"""
file_name = input("Test name: ")
data_path = path.join(path.dirname(path.dirname(__file__)), "data")
imu_data_path = path.join(data_path, file_name + "_imu.txt")
gps_data_path = path.join(data_path, file_name + "_gps.txt")

imu_data, first_imu_timestamp = read_into_queue(imu_data_path, "imu")
gps_data, first_gps_timestamp = read_into_queue(gps_data_path, "gps")


if first_imu_timestamp < first_gps_timestamp:
    thread1_data = imu_data
    thread2_data = gps_data
    timestamp_offset = first_gps_timestamp - first_imu_timestamp
else:
    thread1_data = gps_data
    thread2_data = imu_data
    timestamp_offset = first_imu_timestamp - first_gps_timestamp
