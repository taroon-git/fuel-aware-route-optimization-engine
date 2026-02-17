from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.core.cache import cache
from .services import geocode_location, get_route
from .utils import load_fuel_data
from .serializers import RouteRequestSerializer
from django.views.decorators.csrf import csrf_exempt


def home(request):
    return render(request, "index.html")


@api_view(["POST"])
def route_optimizer(request):

    # ✅ Use serializer for validation
    serializer = RouteRequestSerializer(data=request.data)

    if not serializer.is_valid():
        return Response(serializer.errors, status=400)

    start = serializer.validated_data["start"]
    end = serializer.validated_data["end"]

    # Create unique cache key
    cache_key = f"route_{start}_{end}"

    # Check cache first
    cached_response = cache.get(cache_key)
    if cached_response:
        return Response(cached_response)

    try:
        # Geocode locations
        start_data = geocode_location(start)
        end_data = geocode_location(end)

        # USA validation
        if (
            start_data["country"] != "United States"
            or end_data["country"] != "United States"
        ):
            return Response(
                {"error": "Both start and end locations must be within the USA."},
                status=400
            )

        start_coords = (start_data["lat"], start_data["lon"])
        end_coords = (end_data["lat"], end_data["lon"])

        # ONE routing API call
        route_data = get_route(start_coords, end_coords)

        route_summary = route_data["routes"][0]["summary"]
        route_geometry = route_data["routes"][0]["geometry"]

        distance_meters = route_summary["distance"]
        distance_miles = distance_meters / 1609.34

        MPG = 10
        MAX_RANGE = 500

        stops_required = int(distance_miles // MAX_RANGE)

        fuel_data = load_fuel_data("fuel-prices-for-be-assessment.csv")

        if not fuel_data:
            return Response(
                {"error": "Fuel data not found."},
                status=500
            )

        cheapest_station = min(fuel_data, key=lambda x: x["price"])

        fuel_stops = []

        for _ in range(stops_required):
            gallons_needed = MAX_RANGE / MPG
            stop_cost = gallons_needed * cheapest_station["price"]

            fuel_stops.append({
                "city": cheapest_station["city"],
                "state": cheapest_station["state"],
                "price_per_gallon": round(cheapest_station["price"], 3),
                "gallons_filled": round(gallons_needed, 2),
                "cost": round(stop_cost, 2)
            })

        total_fuel_cost = sum(stop["cost"] for stop in fuel_stops)

        response_data = {
            "start": start,
            "end": end,
            "distance_miles": round(distance_miles, 2),
            "fuel_stops": fuel_stops,
            "total_fuel_cost": round(total_fuel_cost, 2),
            "route_geometry": route_geometry
        }

        # Save to cache
        cache.set(cache_key, response_data, timeout=3600)

        return Response(response_data)

    except Exception as e:
        return Response({"error": str(e)}, status=500)
