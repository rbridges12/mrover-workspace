import json
import sys

KML_HEADER = """<?xml version="1.0" encoding="UTF-8"?>
                    <kml xmlns="http://www.opengis.net/kml/2.2">
                        <Document id="1">"""
KML_FOOTER = """        </Document>
                    </kml>"""


def parse_gps_data(gps_filename):
    with open(gps_filename, "r") as f:
        raw_msgs = f.read().split("\n\n")

        msgs = []
        for raw_msg in raw_msgs:

            # remove timestamp (first line of each msg)
            raw_msg = "".join(raw_msg.split("\n")[1:])

            # replace single quotes with double quotes for JSON
            raw_msg = raw_msg.replace("\'", "\"")

            if raw_msg != "":
                msgs.append(json.loads(raw_msg))
    return msgs


def new_placemark(lon, lat, name=0, id=0):
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
        placemarks.append(new_placemark(lon, lat, i, i))

    with open(kml_filename, 'w') as f:
        f.write(KML_HEADER + "\n".join(placemarks) + KML_FOOTER)


gps_file = "data/" + sys.argv[1]
kml_file = "data/" + sys.argv[1].replace(".txt", ".kml")
data = parse_gps_data(gps_file)
export_kml(data, kml_file)
