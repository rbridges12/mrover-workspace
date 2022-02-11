import json
from os import times

def parse_imu_data(imu_filename):
    with open(imu_filename, "r") as f:
        raw_msgs = f.read().split("\n\n")

        msgs = []
        for raw_msg in raw_msgs:

            # separate timestamp from LCM struct
            lines = raw_msg.split("\n")
            timestamp_str = lines[0]
            raw_msg = "".join(lines[1:])

            # replace single quotes with double quotes for JSON
            raw_msg = raw_msg.replace("\'", "\"")

            if raw_msg != "":
                msg = json.loads(raw_msg)
                msg["timestamp"] = timestamp_str
    return msgs


