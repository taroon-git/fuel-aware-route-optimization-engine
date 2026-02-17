from django.test import TestCase
from rest_framework.test import APIClient
from django.urls import reverse
from unittest.mock import patch


class RouteOptimizerTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.url = "/api/optimize-route/"

    @patch("route_api.services.get_route")
    @patch("route_api.services.geocode_location")
    def test_valid_route_request(self, mock_geocode, mock_route):
        # Mock geocode response
        mock_geocode.side_effect = [
            {"lat": 32.7767, "lon": -96.7970, "country": "United States"},
            {"lat": 29.7604, "lon": -95.3698, "country": "United States"},
        ]

        # Mock route response
        mock_route.return_value = {
            "routes": [{
                "summary": {"distance": 400000},
                "geometry": "encoded_polyline"
            }]
        }

        response = self.client.post(self.url, {
            "start": "Dallas, TX",
            "end": "Houston, TX"
        }, format="json")

        self.assertEqual(response.status_code, 200)
        self.assertIn("distance_miles", response.data)
        self.assertIn("total_fuel_cost", response.data)

    @patch("route_api.services.geocode_location")
    def test_non_usa_location(self, mock_geocode):
        mock_geocode.side_effect = [
            {"lat": 43.6510, "lon": -79.3470, "country": "Canada"},
            {"lat": 29.7604, "lon": -95.3698, "country": "United States"},
        ]

        response = self.client.post(self.url, {
            "start": "Toronto",
            "end": "Houston, TX"
        }, format="json")

        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.data)

    def test_missing_fields(self):
        response = self.client.post(self.url, {}, format="json")
        self.assertEqual(response.status_code, 400)
