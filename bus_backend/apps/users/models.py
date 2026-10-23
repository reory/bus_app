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

class UserFavourite(models.Model):
    """
    Allows users to pin specific stops IDs 
    and routes to their personalised dashboard.
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="favourites")
    stop_id = models.CharField(max_length=50)
    route_id = models.CharField(max_length=50, blank=True, null=True)
    nickname = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-created_at",)

    def __str__(self):
        return f"{self.user.username} -> Stop {self.stop_id} ({self.nickname or 'Pinned'})"