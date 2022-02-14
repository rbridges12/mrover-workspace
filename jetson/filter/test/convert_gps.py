import enum
import json
import sys

KML_HEADER = """<?xml version="1.0" encoding="UTF-8"?>
                    <kml xmlns="http://www.opengis.net/kml/2.2">
                        <Document id="1">"""
KML_FOOTER = """        </Document>
                    </kml>"""


def parse_gps_data(gps_filename):
    with open(gps_filename, "r") as f:
        raw_msgs = f.read().strip().split("\n\n")

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

    return msgs


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
gps_file = sys.argv[1]
kml_file = sys.argv[1].replace(".txt", ".kml")
data = parse_gps_data(gps_file)
export_kml(data, kml_file)
