import pytest
from unittest.mock import patch, MagicMock
from kivy.clock import Clock
import time

from frontend.screens.routes_screen import RoutesScreen

class MockManager:
    """Mock for ScreenManager to test navigation."""
    def __init__(self):
        self.current = "routes"
        # We create a specific mock for the stops screen here
        self.stops_screen = MagicMock()
    
    def get_screen(self, name):
        if name == "stops":
            return self.stops_screen
        return MagicMock()

@pytest.fixture
def routes_screen():
    screen = RoutesScreen(name="routes")
    screen.manager = MockManager()
    return screen

def test_initial_state(routes_screen):
    """Ensure properties start empty."""
    assert routes_screen.routes == []
    assert routes_screen.rv_data == []

@patch('frontend.screens.routes_screen.get_routes')
def test_load_routes_populates_rv_data(mock_get_routes, routes_screen):
    """Verify that rv_data is correctly formatted after an API call."""
    
    # 1. Setup Mock Data as a PLAIN list (not a coroutine)
    mock_data = [
        {"route_id": "101", "short_name": "101", "long_name": "Express"}
    ]
    mock_get_routes.return_value = mock_data

    # 2. Trigger the load
    routes_screen.on_pre_enter()

    # 3. Wait for the background thread and Clock.schedule_once
    timeout = 3
    start_time = time.time()
    while not routes_screen.rv_data and time.time() - start_time < timeout:
        Clock.tick()
        time.sleep(0.1)

    # 4. Assertions
    assert len(routes_screen.routes) == 1
    assert routes_screen.rv_data[0]["route_id"] == "101"
    assert routes_screen.rv_data[0]["text"] == "101 - Express"

def test_select_route_navigation(routes_screen):
    """Check if selecting a route updates the manager correctly."""
    # This calls routes_screen.manager.get_screen("stops")
    routes_screen.select_route("R99")
    
    # Check if the route_id was set on our manager's stops_screen mock
    assert routes_screen.manager.stops_screen.route_id == "R99"
    assert routes_screen.manager.current == "stops"