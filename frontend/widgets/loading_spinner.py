# Loading spinner can be used on any screen in Kivy.
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import BooleanProperty

class LoadingOverlay(BoxLayout):
    """A full screen dimmed overlay with a spinner."""

    # When True, dims the screen and shows the spinner.
    active = BooleanProperty(False)