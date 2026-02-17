import requests
from django.conf import settings

API_KEY = settings.ORS_API_KEY


def geocode_location(place):
    """
    Geocode a location string using OpenRouteService.
    Returns latitude, longitude and country.
    """

    url = "https://api.openrouteservice.org/geocode/search"

    params = {
        "api_key": API_KEY,
        "text": place,
        "size": 1
    }

    response = requests.get(url, params=params)

    if response.status_code != 200:
        raise Exception("Geocoding API request failed")

    data = response.json()

    if "features" not in data or len(data["features"]) == 0:
        raise Exception("Location not found")

    feature = data["features"][0]

    coordinates = feature["geometry"]["coordinates"]
    country = feature["properties"].get("country")

    return {
        "lat": coordinates[1],   # latitude
        "lon": coordinates[0],   # longitude
        "country": country
    }


def get_route(start_coords, end_coords):
    """
    Get driving route between two coordinate points.
    Only ONE routing API call per request (assignment requirement).
    """

    url = "https://api.openrouteservice.org/v2/directions/driving-car"

    headers = {
        "Authorization": API_KEY,
        "Content-Type": "application/json"
    }

    body = {
        "coordinates": [
            [start_coords[1], start_coords[0]],  # [lon, lat]
            [end_coords[1], end_coords[0]]
        ]
    }

    response = requests.post(url, json=body, headers=headers)

    if response.status_code != 200:
        raise Exception("Routing failed. Please verify locations.")

    return response.json()
