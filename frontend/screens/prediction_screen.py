from kivy.uix.screenmanager import Screen
from kivy.properties import StringProperty, DictProperty
from kivy.clock import Clock
import threading

from services.api import get_prediction
from widgets.error_popup import ErrorPopup


class PredictionScreen(Screen):
    """Screen responsible for showing arrival time predictions."""
    
    # Passed in from the StopsScreen.
    stop_id = StringProperty("")
    route_id = StringProperty("")
    
    # Prediction data from backend.
    prediction = DictProperty({})

    def on_pre_enter(self):
        """Called automatically when the screen is about to be shown."""
        print(f"PredictionScreen: on_pre_enter called with stop_id={self.stop_id}, route_id={self.route_id}")
        Clock.schedule_once(lambda dt: self.load_prediction(), 0)

    def load_prediction(self):
        """Start loading prediction in a background thread."""
        print(f"PredictionScreen: load_prediction called")
        
        if not self.stop_id or not self.route_id:
            print("PredictionScreen: stop_id or route_id missing")
            return
        
        def fetch_data():
            data = None
            try:
                import asyncio
                # Create a new event loop for this thread
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                data = loop.run_until_complete(get_prediction(self.route_id, self.stop_id))
                loop.close()
                
                print(f"PredictionScreen: Fetched data: {data}")
            except Exception as e:
                print(f"PredictionScreen: Error loading prediction: {e}")
                data = None
            
            # If data is empty or error occurred, use dummy data
            # Fallback dummy data used only if API fails (IMPORTANT)
            if not data:
                print("PredictionScreen: Using dummy data")
                data = {
                    "stop_name": "Main Street Station",
                    "route_name": "Route 1 - Downtown Express",
                    "arrival_time": "5 minutes",
                    "next_arrival": "15 minutes",
                    "status": "On Time"
                }
            
            # Schedule UI update on main thread
            Clock.schedule_once(lambda dt: self.update_prediction(data), 0)
        
        # Run in background thread
        threading.Thread(target=fetch_data, daemon=True).start()

    def update_prediction(self, data):
        """Update UI with fetched prediction (runs on main thread)."""
        print(f"PredictionScreen: update_prediction called with data: {data}")
        self.prediction = data

    def go_back_stops(self):
        """Return to the StopsScreen."""
        self.manager.current = "stops"

    def show_error(self, message: str):
        popup = ErrorPopup(message=message)
        popup.open()