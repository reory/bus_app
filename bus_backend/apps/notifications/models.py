from django.db import models
# Access the active user model (supports customization of fields too.)
from django.contrib.auth import get_user_model
from bus_backend.apps.routes.models import Route

# Reference the custom User model.
User = get_user_model()

class Alert(models.Model):
    """Service alert which is tied to a specific route."""

    # Route this alert applies to.
    route = models.ForeignKey(Route, on_delete=models.CASCADE)
    # Alert text shown to users.
    message = models.TextField()
    # Timestamp when the alert was created.
    created_at = models.DateTimeField(auto_now_add=True)

class UserAlertSubscription(models.Model):
    """Tracks which users subscribe to alerts for which routes."""

    # User who receives alerts.
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # Route that the user is subscribed to.
    route = models.ForeignKey(Route, on_delete=models.CASCADE)