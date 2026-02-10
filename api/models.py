from django.db import models

"""
API projection models.

These models are derived from GTFS truth and are safe to delete and rebuild.
Do NOT infer transit meaning from these models.
"""

class Route(models.Model):

    # Use a short string ID - "5" or "C32" instead of auto-increment.
    route_id = models.CharField(primary_key=True, max_length=20)
    # Human readable route name which is shown in the UI (Kivy app)
    short_name = models.CharField(max_length=100)
    # Full descriptive name like "Bus stop highway"
    long_name = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.short_name} - {self.long_name}"

class Stop(models.Model):

    # Stop IDs come from external sources. so keep them as a string.
    stop_id = models.CharField(primary_key=True, max_length=20)
    # Each stop belongs to a single route.
    route = models.ForeignKey(
        Route, 
        # Delete stops automatically if the route is removed.
        on_delete=models.CASCADE, 
        # Allows route.stops to access all stops for a route.
        related_name="stops"
    )
    # Display name for the stop.
    name = models.CharField(max_length=100)
    # Order of the stop along the route (derived from the GTFS sequence.)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order"]

class Alert(models.Model):
    
    # Full alert text - delays, closures, warnings, etc.
    message = models.TextField()
    severity = models.CharField(
        max_length=10,
        choices=[
            ("info", "Info"),
            ("warning", "Warning"),
            ("critical", "Critical"),
        ],
        default="info"
    )
    route = models.ForeignKey(
        Route,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    active = models.BooleanField(default=True)
    # Timestamp automatically set when the alert is created.
    created_at = models.DateTimeField(auto_now_add=True)
    
