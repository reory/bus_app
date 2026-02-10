import pytest
# Updated import to match your bus_backend/apps/routes/ structure
from api.models import Route, Stop, Alert

@pytest.mark.django_db
class TestTransitModels:

    def test_route_creation(self):
        route = Route.objects.create(
            route_id="B1", 
            short_name="Blue Line", 
            long_name="Downtown to Airport"
        )
        assert str(route) == "Blue Line - Downtown to Airport"

    def test_stop_ordering_and_relationship(self):
        """
        Using Stop.objects.filter instead of the reverse 'route.stops' 
        to avoid IDE linting errors.
        """
        route = Route.objects.create(route_id="R1", short_name="Red", long_name="Red Line")
        
        Stop.objects.create(stop_id="S2", name="Second Stop", route=route, order=2)
        Stop.objects.create(stop_id="S1", name="First Stop", route=route, order=1)

        # We query the Stop model directly filtering by the route object
        stops = Stop.objects.filter(route=route).order_by('order')
        
        assert stops.count() == 2
        assert stops[0].stop_id == "S1"
        assert stops[1].stop_id == "S2"

    def test_cascade_deletion(self):
        route = Route.objects.create(route_id="G1", short_name="Green", long_name="Green Line")
        Stop.objects.create(stop_id="GS1", name="Green Stop", route=route, order=1)
        
        route.delete()
        
        # Verify that the stop was deleted along with the route
        assert Stop.objects.filter(stop_id="GS1").count() == 0

    def test_alert_logic(self):
        route = Route.objects.create(route_id="Y1", short_name="Yellow", long_name="Yellow Line")
        alert = Alert.objects.create(message="Delay", route=route, severity="warning")
        
        assert alert.route.short_name == "Yellow"
        assert alert.active is True