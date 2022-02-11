# from os import path
from rover_msgs import IMUData, GPS
import json
import time
from datetime import datetime
from queue import Queue
import threading
import lcm


IMU_DATA_SIZE = 13
GPS_DATA_SIZE = 7

lcm_ = lcm.LCM()  # TODO: Compare this vs rover_common/aiolcm


def read_into_queue(file_path, data_type):
    queue = Queue()
    with open(file_path, "r") as f:
        while True:
            timestamp = f.readline()
            if not timestamp:
                break
            timestamp_sec = datetime.strptime(
                timestamp, "----- %Y-%m-%d %H:%M:%S.%f\n").timestamp()
            json_string = ""
            for _ in range(IMU_DATA_SIZE if data_type == "imu" else GPS_DATA_SIZE):
                json_string += f.readline()
            f.readline()
            json_string = json_string.replace("\n", "").replace("\'", "\"")
            json_obj = json.loads(json_string)

            lcm = IMUData() if data_type == "imu" else GPS()
            for key, val in json_obj.items():
                setattr(lcm, key, val)
            queue.put((lcm, timestamp_sec))
    return queue


def send_lcms_from_queue(data_queue, lcm_name):
    while not data_queue.empty():
        datum = data_queue.get()
        lcm_to_send = datum[0]
        curr_timestamp = datum[1]
        lcm_.publish(lcm_name, lcm_to_send.encode())
        print("Published LCM to " + lcm_name + " at " + str(curr_timestamp))
        if not data_queue.empty():
            time.sleep(data_queue.queue[0][1] - curr_timestamp)


"""
Opens specified test file then processes data into queues

Test files must be named: NAME_imu.txt and NAME_gps.txt

imu/gps_data are Queues of their respective LCM objects
first_imu/gps_timestamp are the timestamp of the first recorded LCM data in microseconds
"""


def main():
    # file_name = "playback"
    # data_path = path.join(path.dirname(path.dirname(__file__)), "data")
    # imu_data_path = path.join(data_path, file_name + "_imu.txt")
    # gps_data_path = path.join(data_path, file_name + "_gps.txt")
    dir_path = "/mnt/jetson/filter_playback/src/data/"
    imu_data_path = dir_path + "playback_imu.txt"
    gps_data_path = dir_path + "playback_gps.txt"

    imu_data = read_into_queue(imu_data_path, "imu")
    gps_data = read_into_queue(gps_data_path, "gps")

    if imu_data.queue[0][1] < gps_data.queue[0][1]:
        thread1_data = imu_data
        thread2_data = gps_data
        thread1_lcm_name = "/imu_data"
        thread2_lcm_name = "/gps"
        timestamp_offset = gps_data.queue[0][1] - imu_data.queue[0][1]
    else:
        thread1_data = gps_data
        thread2_data = imu_data
        thread1_lcm_name = "/gps"
        thread2_lcm_name = "/imu_data"
        timestamp_offset = imu_data.queue[0][1] - gps_data.queue[0][1]

    thread1 = threading.Thread(
        target=send_lcms_from_queue, args=(thread1_data, thread1_lcm_name))
    thread2 = threading.Thread(
        target=send_lcms_from_queue, args=(thread2_data, thread2_lcm_name))

    thread1.start()
    time.sleep(timestamp_offset)
    thread2.start()


if __name__ == "__main__":
    main()
