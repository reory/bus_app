from kivy.uix.screenmanager import Screen
from kivy.properties import ListProperty, StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
import threading

from services.api import get_alerts
from widgets.error_popup import ErrorPopup


class AlertsScreen(Screen):
    """Screen for displaying service alerts."""
    
    # Reactive list of service alerts loaded from the backend.
    alerts = ListProperty([])
    
    # Track which screen we came from
    previous_screen = StringProperty("routes")

    def on_pre_enter(self):
        """Called automatically when the screen is about to be shown."""
        print(f"AlertsScreen: on_pre_enter called, came from: {self.previous_screen}")
        Clock.schedule_once(lambda dt: self.load_alerts(), 0)

    def load_alerts(self):
        """Start loading alerts in a background thread."""
        print("AlertsScreen: load_alerts called")
        
        def fetch_data():
            data = None
            try:
                import asyncio
                # Create a new event loop for this thread
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                data = loop.run_until_complete(get_alerts())
                loop.close()
                
                print(f"AlertsScreen: Fetched data: {data}")
            except Exception as e:
                print(f"AlertsScreen: Error loading alerts: {e}")
                data = None
            
            # If data is empty or error occurred, use dummy data
            if not data:
                print("AlertsScreen: Using dummy data")
                data = [
                    {
                        "alert_id": "1",
                        "title": "Route 1 Delay",
                        "description": "Due to construction on Main Street, Route 1 is experiencing 10-minute delays.",
                        "severity": "warning"
                    },
                    {
                        "alert_id": "2",
                        "title": "Route 2 Detour",
                        "description": "Route 2 is temporarily detouring around the parade downtown.",
                        "severity": "info"
                    },
                    {
                        "alert_id": "3",
                        "title": "Holiday Schedule",
                        "description": "All routes will run on Sunday schedule for the upcoming holiday.",
                        "severity": "info"
                    },
                ]
            
            # Schedule UI update on main thread
            Clock.schedule_once(lambda dt: self.update_alerts(data), 0)
        
        # Run in background thread
        threading.Thread(target=fetch_data, daemon=True).start()

    def update_alerts(self, data):
        """Update UI with fetched alerts (runs on main thread)."""
        print(f"AlertsScreen: update_alerts called with {len(data)} alerts")
        self.alerts = data

    def go_back(self):
        """Return to the previous screen."""
        print(f"AlertsScreen: Going back to {self.previous_screen}")
        self.manager.current = self.previous_screen

    def select_alert(self, alert):
        """Called when a user taps an alert."""
        print(f"AlertsScreen: Selected alert: {alert}")

    def show_error(self, message: str):
        popup = ErrorPopup(message=message)
        popup.open()

class AlertItem(BoxLayout):
    title = StringProperty("")
    description = StringProperty("")
    severity = StringProperty("info")