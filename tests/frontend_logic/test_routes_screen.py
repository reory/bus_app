import time
from unittest.mock import MagicMock, patch

import pytest
import respx
from kivy.clock import Clock

from frontend.screens.routes_screen import RoutesScreen


class MockManager:
    """Mock for ScreenManager to test navigation."""

    def __init__(self):
        self.current = "routes"
        # Create a specific mock for the stops screen here
        self.stops_screen = MagicMock()

    def get_screen(self, name):
        if name == "stops":
            return self.stops_screen
        return MagicMock()


@pytest.fixture
def routes_screen():
    """Return the screen that displays available routes."""

    screen = RoutesScreen(name="routes")
    screen.manager = MockManager()
    return screen


def test_initial_state(routes_screen):
    """Ensure properties start empty."""

    assert routes_screen.routes == []
    assert routes_screen.rv_data == []


@patch("frontend.screens.routes_screen.get_routes")
def test_load_routes_populates_rv_data(mock_get_routes, routes_screen):
    """Verify that rv_data is correctly formatted after an API call."""

    # Setup Mock Data as a PLAIN list (not a coroutine)
    mock_data = [{"route_id": "101", "short_name": "101", "long_name": "Express"}]
    mock_get_routes.return_value = mock_data

    # rigger the load
    routes_screen.on_pre_enter()

    # Wait for the background thread and Clock.schedule_once
    timeout = 3
    start_time = time.time()
    while not routes_screen.rv_data and time.time() - start_time < timeout:
        Clock.tick()
        time.sleep(0.1)

    # Assertions
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


@pytest.mark.asyncio
@respx.mock
@patch("frontend.screens.routes_screen.get_favourites")
@patch("frontend.screens.routes_screen.get_routes")
def test_load_favourites_populates_list(mock_get_routes, mock_get_favourites, routes_screen):
    """Verify that favourites property is correctly populated after an API call."""

    # Provide valid route data to prevent KeyErrors during route loading lifecycle
    mock_get_routes.return_value = [{"route_id": "1", "short_name": "1", "long_name": "Express", "route_type": 3}]
    mock_get_favourites.return_value = [{"stop_id": "S102", "route_id": "1", "nickname": "Work"}]

    routes_screen.on_pre_enter()

    timeout = 3
    start_time = time.time()
    while not routes_screen.favourites and time.time() - start_time < timeout:
        Clock.tick()
        time.sleep(0.1)

    assert len(routes_screen.favourites) == 1
    assert routes_screen.favourites[0]["nickname"] == "Work"


def test_select_favourite_navigation(routes_screen):
    """Check if selecting a favourite updates the prediction screen manager correctly."""

    routes_screen.manager.prediction_screen = MagicMock()
    # Mock manager to return prediction screen when requested
    routes_screen.manager.get_screen = lambda name: routes_screen.manager.prediction_screen if name == "prediction" else MagicMock()

    class MockFavourite:
        stop_id = "S102"
        route_id = "1"

    routes_screen.select_favourite(MockFavourite())

    assert routes_screen.manager.prediction_screen.stop_id == "S102"
    assert routes_screen.manager.prediction_screen.route_id == "1"
    assert routes_screen.manager.current == "prediction"
