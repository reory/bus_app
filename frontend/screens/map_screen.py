from pathlib import Path
from kivy.uix.screenmanager import Screen
from widgets.map_pin import MapPin
from utils.constants import STOP_POSITIONS

class MapScreen(Screen):

    stop_id = ""
    stop_name = ""

    def on_pre_enter(self):

        image = self.ids.map_image
        image.source = ""
        
        path = Path(f"assets/maps/{self.stop_id}.png")

        if path.exists():
            self.ids.map_image.source = str(path)
        else: 
            self.ids.map_image.source = "assets/maps/default.png"

        image.reload()

        # Load pin layer setup ---------------------

        # Clear everything in the map container.
        self.ids.map_container.clear_widgets()

        # re-add the map image first.
        self.ids.map_container.add_widget(image)

        pos = STOP_POSITIONS.get(self.stop_id, {"x": 0.5, "y": 0.5})

        # Add a test pin on top of the image.
        pin = MapPin(
            source ="assets/maps/pin.png",
            size_hint=(None, None),
            size=(48, 48),
            pos_hint=pos,
            stop_id=self.stop_id
        )
        
        # Add pin to the map.
        self.ids.map_container.add_widget(pin)

    def go_back(self):
        # Go back to the stops screen.
        self.manager.current = "stops"

