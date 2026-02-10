import sys
import os
from pathlib import Path

# Force the bus_app root into the path.
root = Path(__file__).resolve().parent.parent.parent.parent
sys.path.insert(0, str(root))

import pytest
import respx
from httpx import Response
from frontend.services.api import get_routes, get_prediction, BASE_URL

@pytest.mark.asyncio
@respx.mock
async def test_get_routes_success():
    """Verify get_routes calls the correct URL and returns JSON."""
    # 1. Mock the backend response
    route_data = [{"route_id": "1", "text": "Route 1"}]
    respx.get(f"{BASE_URL}/api/routes/").mock(return_value=Response(200, json=route_data))

    # 2. Call the frontend service
    result = await get_routes()

    # 3. Assertions
    assert result == route_data
    assert len(result) == 1
    assert result[0]["route_id"] == "1"

@pytest.mark.asyncio
@respx.mock
async def test_get_prediction_format():
    """Verify prediction service handles the route/stop URL parameters."""
    stop_id = "S123"
    route_id = "R55"
    mock_response = {"arrival_time": "5 min", "status": "On time"}
    
    # Mock the specific parameterized URL
    respx.get(f"{BASE_URL}/api/predictions/{route_id}/{stop_id}/").mock(
        return_value=Response(200, json=mock_response)
    )

    result = await get_prediction(stop_id, route_id)
    assert result["arrival_time"] == "5 min"

@pytest.mark.asyncio
@respx.mock
async def test_api_error_handling():
    """Test what happens if the Django server is down (500 error)."""
    respx.get(f"{BASE_URL}/api/alerts/").mock(return_value=Response(500))

    # Since you use r.raise_for_status(), it should raise an exception
    from httpx import HTTPStatusError
    with pytest.raises(HTTPStatusError):
        from frontend.services.api import get_alerts
        await get_alerts()