from kivy.uix.modalview import ModalView
from kivy.properties import StringProperty

class ErrorPopup(ModalView):
    """Reusable themed popup for displaying error messages."""

    message = StringProperty("")