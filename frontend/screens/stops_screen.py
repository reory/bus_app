from kivy.uix.screenmanager import Screen
from kivy.properties import StringProperty, ListProperty
from kivy.clock import Clock
import threading

from services.api import get_stops
from widgets.error_popup import ErrorPopup


class StopsScreen(Screen):
    """Screen for listing stops for the selected route."""
    
    # Passed in from RoutesScreen before switching screens.
    route_id = StringProperty("")
    
    # list of stops returned from the backend
    stops = ListProperty([])

    def on_pre_enter(self):
        """Called automatically when the screen is about to be shown."""
        print(f"StopsScreen: on_pre_enter called with route_id={self.route_id}")
        Clock.schedule_once(lambda dt: self.load_stops(), 0)

    def load_stops(self):
        """Start loading stops in a background thread."""
        print(f"StopsScreen: load_stops called for route_id={self.route_id}")
        
        if not self.route_id:
            print("StopsScreen: route_id not set")
            return
        
        def fetch_data():
            data = None
            try:
                import asyncio
                # Create a new event loop for this thread
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                data = loop.run_until_complete(get_stops(self.route_id))
                loop.close()
                
                print(f"StopsScreen: Fetched data: {data}")
            except Exception as e:
                print(f"StopsScreen: Error loading stops: {e}")
                data = None
            
            # If data is empty or error occurred, use dummy data
            if not data:
                print("StopsScreen: Using dummy data")
                data = [
                    {"stop_id": "101", "name": "Main Street Station"},
                    {"stop_id": "102", "name": "City Hall"},
                    {"stop_id": "103", "name": "Central Park"},
                    {"stop_id": "104", "name": "University Campus"},
                    {"stop_id": "105", "name": "Shopping Mall"},
                ]
            
            # Schedule UI update on main thread
            Clock.schedule_once(lambda dt: self.update_stops(data), 0)
        
        # Run in background thread
        threading.Thread(target=fetch_data, daemon=True).start()

    def update_stops(self, data):
        """Update UI with fetched stops (runs on main thread)."""
        print(f"StopsScreen: update_stops called with {len(data)} stops")
        self.stops = data

    def select_stop(self, stop_id):
        """Called when a user taps a stop."""
        print(f"StopsScreen: select_stop called with stop_id={stop_id}")
        # Access the prediction instance.
        prediction_screen = self.manager.get_screen("prediction")
        # Pass selected stop to prediction screen.
        prediction_screen.stop_id = stop_id
        # Pass current route to prediction screen.
        prediction_screen.route_id = self.route_id
        # Navigate to the prediction screen.
        self.manager.current = "prediction"

    def show_error(self, message: str):
        popup = ErrorPopup(message=message)
        popup.open()

    def view_on_map(self, stop):
        map_screen = self.manager.get_screen("map")
        
        map_screen.stop_id = stop.get("stop_id", "").strip()
        map_screen.stop_name = stop.get("name", "Bus Stop")

        self.manager.current = "map"