import math
import polyline
import os
import csv

def load_fuel_data(file_name):
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    file_path = os.path.join(BASE_DIR, file_name)

    fuel_data = []

    with open(file_path, newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)

        for row in reader:
            try:
                fuel_data.append({
                    "city": row["City"],
                    "state": row["State"],
                    "price": float(row["Retail Price"])
                })
            except:
                continue

    return fuel_data






def decode_route_geometry(encoded_geometry):
    return polyline.decode(encoded_geometry)


def haversine(lat1, lon1, lat2, lon2):
    R = 3958.8  # Earth radius in miles

    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)

    a = math.sin(dlat / 2) ** 2 + \
        math.cos(math.radians(lat1)) * \
        math.cos(math.radians(lat2)) * \
        math.sin(dlon / 2) ** 2

    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    return R * c
