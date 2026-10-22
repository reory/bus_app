# Loading spinner can be used on any screen in Kivy.
from kivy.properties import BooleanProperty
from kivy.uix.boxlayout import BoxLayout


class LoadingOverlay(BoxLayout):
    """A full screen dimmed overlay with a spinner."""

    # When True, dims the screen and shows the spinner.
    active = BooleanProperty(False)