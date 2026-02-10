from kivy.uix.image import Image
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.properties import StringProperty
from utils.constants import STOP_NAMES

class MapPin(ButtonBehavior, Image):
    
    stop_id = StringProperty("")

    def on_release(self):

        stop_name = STOP_NAMES.get(self.stop_id, self.stop_id)

        popup = Popup(
            title="Bus Stop",
            content=Label(text=stop_name, font_size=20),
            size_hint=(0.6, 0.3)
        )

        popup.open()