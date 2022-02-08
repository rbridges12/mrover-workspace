from ast import parse
import json
import sys
import simplekml

EARTH_RADIUS_M = 6371000

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

def export_kml(gps_json, kml_filename):
    kml = simplekml.Kml()
    for point in gps_json:
        lat_decimal = point["latitude_deg"] + point["latitude_min"] / 60
        lon_decimal = point["longitude_deg"] + point["longitude_min"] / 60
        kml.newpoint(name=point["timeStamp"], coords=[(lon_decimal, lat_decimal)])
        kml.save(kml_filename)

gps_file = "data/" + sys.argv[1]
kml_file = "data/" + sys.argv[1].replace(".txt", ".kml")
data = parse_gps_data(gps_file)
export_kml(data, kml_file)
