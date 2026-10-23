import threading

from kivy.clock import Clock
from kivy.properties import ListProperty, StringProperty
from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen
from services.api import get_favourites, get_routes
from widgets.error_popup import ErrorPopup


class RoutesScreen(Screen):
    """
    The main application screen displaying available 
    transit routes and pinned favourite commutes.
    """

    # List of routes returned from backend
    routes = ListProperty([])

    # Data formatted for RecycleView
    rv_data = ListProperty([])

    # List of pinned favourite stops for the personalised dashboard
    favourites = ListProperty([])

    def on_pre_enter(self):
        """Called automatically when the screen is about to be shown."""

        print("RoutesScreen: on_pre_enter called")
        Clock.schedule_once(lambda dt: self.load_routes(), 0)
        Clock.schedule_once(lambda dt: self.load_favourites(), 0)

    def load_routes(self):
        """Start loading routes in a background thread."""

        print("RoutesScreen: load_routes called")

        def fetch_data():
            """Start loading stops in a background thread."""

            try:
                import asyncio

                # Create a new event loop for this thread
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                data = loop.run_until_complete(get_routes())
                loop.close()

                print(f"RoutesScreen: Fetched data: {data}")

                # If data is empty, use dummy data for testing
                if not data:
                    print("RoutesScreen: No data from API, using dummy data")
                    data = [
                        {
                            "route_id": "1",
                            "short_name": "Route 1",
                            "long_name": "Downtown Express",
                        },
                        {
                            "route_id": "2",
                            "short_name": "Route 2",
                            "long_name": "Airport Shuttle",
                        },
                        {
                            "route_id": "3",
                            "short_name": "Route 3",
                            "long_name": "University Line",
                        },
                    ]

                # Schedule UI update on main thread
                Clock.schedule_once(lambda dt: self.update_routes(data), 0)
            except Exception as e: #noqa
                print(f"Error loading routes: {e}")
                Clock.schedule_once(
                    lambda dt: self.show_error(
                        "Unable to load routes. Check your connection."
                    ),
                    0,
                )

        # Run in background thread
        threading.Thread(target=fetch_data, daemon=True).start()

    

        print(f"RoutesScreen: rv_data = {self.rv_data}")


    def select_route(self, route_id):
        """Called when the user taps a route."""

        print(f"RoutesScreen: select_route called with route_id={route_id}")
        stops_screen = self.manager.get_screen("stops")
        stops_screen.route_id = route_id
        self.manager.current = "stops"

    def update_routes(self, data):
        """Update UI with fetched routes (runs on main thread)."""

        print(f"RoutesScreen: update_routes called with {len(data)} routes")
        self.routes = data

        # RecycleView data
        self.rv_data = [
            {"text": f"{r['short_name']} - {r['long_name']}", "route_id": r["route_id"]}
            for r in data
        ]

    def show_error(self, message: str):
        """Display an error message to the user."""

        popup = ErrorPopup(message=message)
        popup.open()

    def select_favourite(self, favourite):
        """Navigate directly to predictions when tapping a pinned favourite."""

        print(f"RoutesScreen: Selected favourite stop {favourite.stop_id}")
        prediction_screen = self.manager.get_screen("prediction")
        prediction_screen.stop_id = favourite.stop_id
        prediction_screen.route_id = favourite.route_id if favourite.route_id else "1"
        self.manager.current = "prediction"

    def load_favourites(self):
        """Load pinned favourites in background thread."""

        print("RoutesScreen: load_favourites called")

        def fetch_favs():
            """Retrieve the user's pinned favourite stops from the backend API."""

            data = []
            try:
                import asyncio
                
                import httpx

                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)

                try:
                    # Fetch favourites and corresponding live predictions
                    data = loop.run_until_complete(get_favourites())
                finally:
                    loop.close()

                # DEBUG PRINT - See what the API actually returns
                print(f"RoutesScreen RAW API Response for favorites: {data}")
            except httpx.HTTPStatusError as e:
                print(f"RoutesScreen: HTTP error loading favourites: {e}")
                Clock.schedule_once(
                    lambda dt: self.show_error("Unable to load favourites from server."),
                    0,
                )
            except Exception as e: #noqa
                print(f"RoutesScreen: Unexpected error loading favourites: {e}")
                import traceback
                traceback.print_exc()
                data = []

            if data is None:
                data = []

            Clock.schedule_once(lambda dt: self.update_favourites(data), 0)

        # Run in a background thread
        threading.Thread(target=fetch_favs, daemon=True).start()

    def update_favourites(self, data):
        """Update the UI with the fetched user favourites data on the main thread."""

        self.favourites = data
        print(f"RoutesScreen: Favourites loaded = {self.favourites}")


class RouteItem(Button):
    """
    A custom interactive button representing a 
    transit route item in the recycle view list.
    """

    route_id = StringProperty("")


class FavouriteItem(Button):
    """View class for individual pinned favourites in the horizontal RecycleView."""

    nickname = StringProperty("")
    stop_id = StringProperty("")
    route_id = StringProperty("")
