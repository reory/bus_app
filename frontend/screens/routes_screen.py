from kivy.uix.screenmanager import Screen
from kivy.properties import ListProperty, StringProperty
from kivy.clock import Clock
from kivy.uix.button import Button
import threading

from frontend.services.api import get_routes
from frontend.widgets.error_popup import ErrorPopup


class RoutesScreen(Screen):
    
    # List of routes returned from backend
    routes = ListProperty([])

    # Data formatted for RecycleView
    rv_data = ListProperty([])

    def on_pre_enter(self):
        """Called automatically when the screen is about to be shown."""
        print("RoutesScreen: on_pre_enter called")
        Clock.schedule_once(lambda dt: self.load_routes(), 0)

    def load_routes(self):
        """Start loading routes in a background thread."""
        print("RoutesScreen: load_routes called")
        
        def fetch_data():
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
                        {"route_id": "1", "short_name": "Route 1", "long_name": "Downtown Express"},
                        {"route_id": "2", "short_name": "Route 2", "long_name": "Airport Shuttle"},
                        {"route_id": "3", "short_name": "Route 3", "long_name": "University Line"},
                    ]
                
                # Schedule UI update on main thread
                Clock.schedule_once(lambda dt: self.update_routes(data), 0)
            except Exception as e:
                print(f"Error loading routes: {e}")
                Clock.schedule_once(lambda dt: self.show_error("Unable to load routes. Check your connection."), 0)
        
        # Run in background thread
        threading.Thread(target=fetch_data, daemon=True).start()

    def update_routes(self, data):
        """Update UI with fetched routes (runs on main thread)."""
        print(f"RoutesScreen: update_routes called with {len(data)} routes")
        self.routes = data
        
        # RecycleView data
        self.rv_data = [
            {
                "text": f"{r['short_name']} - {r['long_name']}",
                "route_id": r["route_id"]
            }
            for r in data
        ]
        
        print(f"RoutesScreen: rv_data = {self.rv_data}")

    def select_route(self, route_id):
        """Called when the user taps a route."""
        print(f"RoutesScreen: select_route called with route_id={route_id}")
        stops_screen = self.manager.get_screen("stops")
        stops_screen.route_id = route_id
        self.manager.current = "stops"

    def show_error(self, message: str):
        popup = ErrorPopup(message=message)
        popup.open()

class RouteItem(Button):
    route_id = StringProperty("")