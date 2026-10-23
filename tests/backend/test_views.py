import time

import pytest
from rest_framework.test import APIClient

from api.models import Alert
from bus_backend.apps.routes.models import Route, Stop, StopTime, Trip


@pytest.fixture
def api_client():
    return APIClient()


@pytest.mark.django_db
class TestViews:
    def test_get_routes(self, api_client):
        """Test the RouteListView returns a 200 and all routes."""

        # Create the base Route using the correct refactored model
        route = Route.objects.create(
            route_id="101", 
            short_name="101", 
            long_name="Express",
            route_type=3
        )
        
        # Create an active trip linked to the unified route model
        Trip.objects.create(trip_id="T_101", route=route)
        
        url = "/api/routes/"
        response = api_client.get(url)
        
        assert response.status_code == 200
        assert len(response.data) == 1


    def test_get_stops_for_route(self, api_client):
        """Test filtering: StopListView should only return stops for that route."""

        # Create the Routes using the refactored model
        r1 = Route.objects.create(route_id="R1", short_name="R1", route_type=3)
        r2 = Route.objects.create(route_id="R2", short_name="R2", route_type=3)
        
        # Create standalone Stops using the refactored model
        s1 = Stop.objects.create(
            stop_id="S1", 
            name="Target Stop",
            lat=53.7999,
            lon=-1.5278
        )
        s2 = Stop.objects.create(
            stop_id="S2", 
            name="Wrong Route Stop",
            lat=53.7855,
            lon=-1.5300
        )
        
        # Connect everything smoothly down the new relational chain
        t1 = Trip.objects.create(trip_id="T1", route=r1)
        StopTime.objects.create(
            trip=t1, 
            stop=s1, 
            stop_sequence=1,
            arrival_time="08:00:00"
        )
        
        t2 = Trip.objects.create(trip_id="T2", route=r2)
        StopTime.objects.create(
            trip=t2, 
            stop=s2, 
            stop_sequence=1,
            arrival_time="08:30:00"
        )
        
        url = "/api/routes/R1/stops/"
        response = api_client.get(url)
        
        assert response.status_code == 200
        assert len(response.data) == 1

    
    def test_prediction_logic(self, api_client):
        """Verify the prediction view returns the expected dictionary structure."""

        url = "/api/predictions/R1/S1/"
        response = api_client.get(url)

        assert response.status_code == 200
        assert "arrival_time" in response.data
        assert "status" in response.data
        assert response.data["arrival_time"].endswith(" min")


    def test_alerts_ordering(self, api_client):
        """Verify alerts are returned newest first."""

        Alert.objects.create(message="Old Alert")

        # Wait 0.1 secs to ensure the timestamp is different
        time.sleep(0.1)

        Alert.objects.create(message="New Alert")

        url = "/api/alerts/"
        response = api_client.get(url)

        assert response.data[0]["description"] == "New Alert"

    def test_user_favourites_get_and_post(self, api_client):
        """Test listing and creating user favourites via the API."""
        from bus_backend.apps.users.models import User, UserFavourite

        user = User.objects.create_user(username="busapp35", password="password")
        UserFavourite.objects.create(
            user=user, stop_id="S102", route_id="1", nickname="Work"
        )

        # Test GET request filtered by username
        response = api_client.get("/api/favourites/?username=busapp35")
        assert response.status_code == 200
        assert len(response.data) == 1
        assert response.data[0]["nickname"] == "Work"
        assert response.data[0]["stop_id"] == "S102"

        # Test POST request to add a new favourite
        payload = {
            "username": "busapp35",
            "stop_id": "S105",
            "route_id": "2",
            "nickname": "Gym"
        }
        post_response = api_client.post("/api/favourites/", payload, format="json")
        assert post_response.status_code == 201
        assert post_response.data["nickname"] == "Gym"
        assert UserFavourite.objects.filter(stop_id="S105").exists()