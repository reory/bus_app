from kivy.properties import StringProperty
from kivy.uix.modalview import ModalView


class ErrorPopup(ModalView):
    """Reusable themed popup for displaying error messages."""

    message = StringProperty("")