from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    """Extend Djangos built-in user model. 
    Allows auth support while allowing the project to grow 
    with custom fields as needed.
    """
    
    # Stores the stop_id of the user's favorite stop.
    # This allows quick access to personalized predictions
    # without needing a lookup table.
    favourite_stop = models.CharField(max_length=50, blank=True)