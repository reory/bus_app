import sys
from unittest.mock import MagicMock, patch

# Inject mock modules into sys.modules to safely intercept top-level screens imports
mock_login = MagicMock()
mock_routes = MagicMock()
mock_stops = MagicMock()
mock_prediction = MagicMock()
mock_alerts = MagicMock()
mock_map = MagicMock()

sys.modules["screens"] = MagicMock()
sys.modules["screens.login_screen"] = mock_login
sys.modules["screens.routes_screen"] = mock_routes
sys.modules["screens.stops_screen"] = mock_stops
sys.modules["screens.prediction_screen"] = mock_prediction
sys.modules["screens.alerts_screen"] = mock_alerts
sys.modules["screens.map_screen"] = mock_map

# Now it's perfectly safe to import the application class
from frontend.main import BusApp #noqa


@patch("frontend.main.Builder")
@patch("frontend.main.ScreenManager")
def test_bus_app_build_lifecycle(mock_screen_manager_cls, mock_builder):
    """Test that BusApp loads all KV themes, screens, and builds the UI matrix properly."""
    
    # Set up our mocked ScreenManager instance
    mock_sm_instance = MagicMock()
    mock_screen_manager_cls.return_value = mock_sm_instance
    
    # Initialize app and run build lifecycle
    app = BusApp()
    root_widget = app.build()
    
    # Assertions: Verify all 7 required .kv layout sheets were loaded
    assert mock_builder.load_file.call_count == 7
    
    # Assertions: Verify all 6 interactive view screens were bound to ScreenManager
    assert mock_sm_instance.add_widget.call_count == 6
    
    # Assertions: Confirm view structure returns clean root instance
    assert root_widget == mock_sm_instance