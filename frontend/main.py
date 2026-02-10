from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from kivy.lang import Builder
import os

# Import screen classes
from screens.login_screen import LoginScreen
from screens.routes_screen import RoutesScreen
from screens.stops_screen import StopsScreen
from screens.prediction_screen import PredictionScreen
from screens.alerts_screen import AlertsScreen
from screens.map_screen import MapScreen

# Import for kivy class registration.
from screens.routes_screen import RouteItem
from screens.alerts_screen import AlertItem

class BusApp(App):
    """Root Kivy application class."""

    def build(self):
        """Construct the root widget for the application"""
        
        # Get the directory where main.py is located
        base_dir = os.path.dirname(os.path.abspath(__file__))
        
        # Load KV files with absolute paths
        print("Loading KV files...")
        
        # Load shared background theme first from the the themes folder.
        Builder.load_file(os.path.join(base_dir, "themes", "themes.kv"))

        # Then load screen-specific KV files.
        Builder.load_file(os.path.join(base_dir, "screens", "loginscreen.kv"))
        Builder.load_file(os.path.join(base_dir, "screens", "routesscreen.kv"))
        Builder.load_file(os.path.join(base_dir, "screens", "stopsscreen.kv"))
        Builder.load_file(os.path.join(base_dir, "screens", "predictionscreen.kv"))
        Builder.load_file(os.path.join(base_dir, "screens", "alertsscreen.kv"))
        Builder.load_file(os.path.join(base_dir, "screens", "mapscreen.kv"))
        
        print("KV files loaded!")
        
        sm = ScreenManager()
        sm.add_widget(LoginScreen(name="login"))
        sm.add_widget(RoutesScreen(name="routes"))
        sm.add_widget(StopsScreen(name="stops"))
        sm.add_widget(PredictionScreen(name="prediction"))
        sm.add_widget(AlertsScreen(name="alerts"))
        sm.add_widget(MapScreen(name="map"))
        
        print(f"ScreenManager screens: {sm.screen_names}")
        
        return sm

    
if __name__ == "__main__":
    BusApp().run()