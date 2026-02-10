from kivy.uix.screenmanager import Screen
# Reactive text value that updates the UI automatically.
from kivy.properties import StringProperty
from widgets.error_popup import ErrorPopup
from kivy.uix.label import Label
from kivy.lang import Builder
import os 

class LoginScreen(Screen):
    """UI screen for handling user login flow."""

    # Hold the entered username and updates the UI automatically.
    username = StringProperty("")
    # Stores the password input as reactive UI value.
    password = StringProperty("")

    def on_enter(self):
        print("LoginScreen: loaded!")

    def do_login(self):
        """Called when the user presses the Login button.
        Later this will call django backend for authentication."""
        
        # TODO: calls backend
        self.manager.current = "routes"

    def show_error(self, message: str):
        popup = ErrorPopup(message=message)
        popup.open()

    

    