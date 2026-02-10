import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from api.models import Route, Stop, Alert
import time

@pytest.fixture
def api_client():
    return APIClient()

@pytest.mark.django_db
class TestViews:

    def test_get_routes(self, api_client):
        """Test the RouteListView returns a 200 and all routes."""
        Route.objects.create(route_id="101", short_name="101", long_name="Express")
        
        # Use the URL name if you have them, or the path
        url = "/api/routes/" 
        response = api_client.get(url)
        
        assert response.status_code == 200
        assert len(response.data) == 1
        assert response.data[0]["route_id"] == "101"

    def test_get_stops_for_route(self, api_client):
        """Test filtering: StopListView should only return stops for that route."""
        r1 = Route.objects.create(route_id="R1", short_name="R1")
        r2 = Route.objects.create(route_id="R2", short_name="R2")
        
        Stop.objects.create(stop_id="S1", name="Target Stop", route=r1)
        Stop.objects.create(stop_id="S2", name="Wrong Route Stop", route=r2)
        
        url = f"/api/routes/R1/stops/"
        response = api_client.get(url)
        
        assert response.status_code == 200
        assert len(response.data) == 1
        assert response.data[0]["stop_id"] == "S1"

    def test_prediction_logic(self, api_client):
        """Verify the prediction view returns the expected dictionary structure."""
        url = "/api/predictions/R1/S1/"
        response = api_client.get(url)
        
        assert response.status_code == 200
        assert "arrival_time" in response.data
        assert "status" in response.data
        # Check that it ends with ' min' as per your f-string
        assert response.data["arrival_time"].endswith(" min")

    def test_alerts_ordering(self, api_client):
        """Verify alerts are returned newest first."""

        Alert.objects.create(message="Old Alert")

        # Wait 0.1 secs to ensure the timestamp is different
        time.sleep(0.1)
        
        Alert.objects.create(message="New Alert")
        
        url = "/api/alerts/"
        response = api_client.get(url)
        
        # In your view you have .order_by("-created_at")
        assert response.data[0]["description"] == "New Alert"