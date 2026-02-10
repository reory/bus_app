from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty, BooleanProperty, ObjectProperty

class HeaderBar(BoxLayout):
    """
    A reusable header widget.
    - Optional back button. (essential)
    - Title text.
    - Optional right side action button.
    """
    
    # Title of the page.
    title = StringProperty("")
    # Back button.
    show_back = BooleanProperty(True)
    # eg Icons, Bells, etc.
    right_icon = StringProperty("")
    # Call back for right button.
    on_right_press = ObjectProperty(None)