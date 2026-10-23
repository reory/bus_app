# Async HTTP client 
# used for making non-blocking API requests to the Django backend.
import httpx

# Local Django server address used for all API requests.
BASE_URL = "http://127.0.0.1:8000"

async def get_routes():
    """Fetch all routes from the Django backend."""
    
    # Open an Async HTTP session for non-blocking API calls.
    async with httpx.AsyncClient() as client:
        # Send GET requests to fetch all routes.
        r = await client.get(f"{BASE_URL}/api/routes/")
        # Throw an error if the server responds with an HTTP failure code.
        r.raise_for_status()
        # Parse and return the JSON response from the backend.
        return r.json()

    
async def get_stops(route_id: str):
    """Fetch stops for a specific route."""

    async with httpx.AsyncClient() as client:
        r = await client.get(f"{BASE_URL}/api/routes/{route_id}/stops/")
        r.raise_for_status()
        return r.json()

    
async def get_prediction(stop_id: str, route_id: str):
    """Fetch the latest prediction for a stop and a route."""

    async with httpx.AsyncClient() as client:
        r = await client.get(
            f"{BASE_URL}/api/predictions/{route_id}/{stop_id}/"
        )
        r.raise_for_status()
        return r.json()


async def get_alerts():
    """Fetch all service alerts."""

    async with httpx.AsyncClient() as client:
        r = await client.get(f"{BASE_URL}/api/alerts/")
        r.raise_for_status()
        return r.json()


async def add_favourite(
    stop_id: str, 
    route_id: str, 
    nickname: str = "Pinned Stop", 
    username: str = "busapp35"
):
    """Send a POST request to pin a favourite stop for the user."""

    url = f"{BASE_URL}/api/favourites/"
    payload = {
        "username": username,
        "stop_id": stop_id,
        "route_id": route_id,
        "nickname": nickname
    }
    print(f"API CLIENT: Adding favourite to {url} with {payload}")

    async with httpx.AsyncClient() as client:
        r = await client.post(url, json=payload)
        print(f"API Client: Add favourite response status = {r.status_code}")
        r.raise_for_status()
        return r.json()


async def get_favourites(username: str = "busapp35"):
    """Fetch pinned favourite stops for the user dashboard."""

    url = f"{BASE_URL}/api/favourites/?username={username}"
    print(f"API CLIENT: Requesting favourites from {url}")

    async with httpx.AsyncClient() as client:
        r = await client.get(url)
        print(f"API Client: Favourites response status = {r.status_code}")
        r.raise_for_status()
        data = r.json()
        print(f"API Client: Favourites data received = {data}")
        return data
    
