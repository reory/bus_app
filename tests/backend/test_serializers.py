import pytest
from api.models import Route, Stop, Alert
from api.serializers import RouteSerializer, StopSerializer, AlertSerializer

@pytest.mark.django_db
class TestSerializers:

    def test_route_serializer_fields(self):
        """Verify Route data is correctly aliased for the UI."""
        route = Route.objects.create(
            route_id="55", 
            short_name="Line 55", 
            long_name="West Side Loop"
        )
        serializer = RouteSerializer(instance=route)
        data = serializer.data

        # Check that 'text' matches 'short_name' as defined in your source="short_name"
        assert data["text"] == "Line 55"
        assert data["route_id"] == "55"
        assert data["long_name"] == "West Side Loop"

    def test_stop_serializer_fields(self):
        """Ensure only the required fields are exposed for Stops."""
        route = Route.objects.create(route_id="1", short_name="1")
        stop = Stop.objects.create(stop_id="S101", name="Main St", route=route)
        
        serializer = StopSerializer(instance=stop)
        
        # 1. Assign the data to the variable first (No 'assert' on this line)
        data = serializer.data
        
        # 2. Now perform your assertions on that data
        assert data["stop_id"] == "S101"
        assert data["name"] == "Main St"
        # Ensure internal fields like 'order' are NOT in the JSON
        assert "order" not in data

    def test_alert_serializer_custom_logic(self):
        """Verify the MethodFields and aliasing in Alerts."""
        alert = Alert.objects.create(
            message="Construction on 5th Ave",
            severity="warning" # This is 'warning' in the DB...
        )
        
        serializer = AlertSerializer(instance=alert)
        data = serializer.data

        # Check the 'description' alias
        assert data["description"] == "Construction on 5th Ave"
        # Check the hardcoded 'get_title' method
        assert data["title"] == "Service Alert"
        # IMPORTANT: Your current serializer hardcodes 'info' 
        # even if the DB says 'warning'. This test confirms that behavior.
        assert data["severity"] == "info"