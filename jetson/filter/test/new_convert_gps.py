import enum
import json
import sys
import os
import pandas as pd

KML_HEADER = """<?xml version="1.0" encoding="UTF-8"?>
                    <kml xmlns="http://www.opengis.net/kml/2.2">
                        <Document id="1">"""
KML_FOOTER = """        </Document>
                    </kml>"""


def parse_gps_data(gps_filename):
    with open(gps_filename, "r") as f:
        raw_msgs = f.read().strip().split("\n\n")
        
        # if last msg is incomplete, get rid of it
        if raw_msgs[-1][-1] != "}":
            raw_msgs = raw_msgs[:-1]

        msgs = []
        for raw_msg in raw_msgs:

            # separate the timestamp from the LCM struct
            lines = raw_msg.split("\n")
            timestamp = lines[0].strip("- ")
            raw_msg = "".join(lines[1:])

            # replace single quotes with double quotes for JSON
            raw_msg = raw_msg.replace("\'", "\"")

            # add or update the timestamp in the JSON object
            # if raw_msg != "":
            msg = json.loads(raw_msg)
            msg["timeStamp"] = timestamp
            msgs.append(msg)

    json_str = json.dumps(msgs)
    f = open("data/json_correct.txt", 'w')
    f.write(json_str)

    return msgs

def parse_gps_data_csv(gps_filename):
    df = pd.read_csv(gps_filename)

    # get only relevant columns
    df = df[["Timestamp", "GPS Degrees Lat", "GPS Minutes Lat", "GPS Degrees Lon", "GPS Minutes Lon"]]

    # rename columns to what they were in the old struct for export to JSON
    df = df.rename(columns=  {"Timestamp"        : "timeStamp", 
                        "GPS Degrees Lat"   : "latitude_deg", 
                        "GPS Minutes Lat"   : "latitude_min", 
                        "GPS Degrees Lon"   : "longitude_deg",
                        "GPS Minutes Lon"   : "longitude_min"})
    
    # convert strings to integers where needed
    df.convert_dtypes()

    raw_json = df.to_json(orient="records")
    msgs = json.loads(raw_json)

    f = open("data/json_test.txt", 'w')
    f.write(raw_json)

    return msgs; 

def kml_placemark(lon, lat, name=0, id=0):
    return f"""<Placemark id="{id}">
                  <name>{name}</name>
                  <Point id="{id}">
                    <coordinates>{lon},{lat},0.0</coordinates>
                  </Point>
               </Placemark>"""


def export_kml(gps_json, kml_filename):
    placemarks = []
    for i, point in enumerate(gps_json):
        lon = point["longitude_deg"] + point["longitude_min"] / 60
        lat = point["latitude_deg"] + point["latitude_min"] / 60
        name = point["timeStamp"]
        placemarks.append(kml_placemark(lon, lat, name, i))

    with open(kml_filename, 'w') as f:
        f.write(KML_HEADER + "\n".join(placemarks) + KML_FOOTER)


"""
Convert an LCM echo log file containing GPS data into a KML file that can be loaded in Google Earth or a similar mapping tool.
Save your LCM log file to a "/data" folder in the same directory as this script,
The KML file will be saved to the same directory with the same name except for a .kml extension.

usage: python3 convert_gps.py [PATH_TO_LCM_FILE]
"""
for filename in os.scandir(sys.argv[1]):
    if filename.is_file():
        if("DS_Store" in filename.path):
            continue; 
        print(filename)
        kml_file = filename.path.replace(".csv", ".kml")
        kml_file = kml_file.replace("logs", "kmls")
        data = parse_gps_data_csv(filename.path)
        export_kml(data, kml_file)

# in sparse mode, only keep every tenth point
#if sys.argv[2] == "-s":
#    data = [pt for i, pt in enumerate(data) if i % 10 == 0]
    
