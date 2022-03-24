from socket import AF_X25
import pandas as pd
import json
import numpy as np
import matplotlib.pyplot as plt
from sys import argv

def read_odom_bearings(csv_filename):
    csv_data = pd.read_csv(csv_filename)

    # get only relevant columns
    csv_data = csv_data[["Odom bearing", "Mag X", "Mag Y", "Mag Z"]]
    
    # convert strings to integers where needed
    # csv_file.convert_dtypes()
    # raw_json = csv_file.to_json(orient="records")
    # msgs = json.loads(raw_json)
    # return msgs

    odom_bearings = csv_data["Odom bearing"].to_list()
    mag_bearings = [mag_to_bearing(row["Mag X"], row["Mag Y"]) for i, row in csv_data.iterrows()]
    return (odom_bearings, mag_bearings)

def mag_to_bearing(mag_x, mag_y):
    raw = np.arctan2(mag_y, mag_x) * (180/np.pi) - 90
    if raw < 0:
        raw += 360    
    return raw
    
odom, mag = read_odom_bearings(argv[1])
#for o, m in zip(odom, mag):
    #print(abs(o - m))
diffs = [abs(o - m) for o, m in zip(odom, mag) if abs(o - m) < 200]

fig, (ax1, ax2) = plt.subplots(1, 2)
fig.suptitle(argv[1].replace("/home/riley/Downloads/", ""))
ax1.plot(range(len(odom)), odom, "b-", label="odometry")
ax1.plot(range(len(mag)), mag, "r-", label="magnetometer")
ax1.set(title="Bearing Over Time", xlabel="row of csv", ylabel="Bearing (deg)")
ax1.legend()
ax2.plot(range(len(diffs)), diffs)
ax2.set(title="Difference between Mag and Odom Bearing Over Time", xlabel="row of csv", ylabel="Error (deg)")
plt.show()