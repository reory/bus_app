from django.db import models
from bus_backend.apps.routes.models import Stop, Route

class VehiclePosition(models.Model):
    """Live location data for a vehicle on a route."""

    # Unique identifier for the vehicle.
    vehicle_id = models. CharField(max_length=50)
    # Link to the route that this vehicle is serving.
    route = models.ForeignKey(Route, on_delete=models.CASCADE)
    # Current latitude of the vehicle.
    lat = models.FloatField()
    # Current longitude of the vehicle.
    lon = models.FloatField()
    # When the vehicle position was recorded.
    timestamp = models.DateTimeField()

class Prediction(models.Model):
    """Arrival time prediction of a route at a stop."""

    # Stop this prediction applies to.
    stop = models.ForeignKey(Stop, on_delete=models.CASCADE)
    # Route associated with this prediction.
    route = models.ForeignKey(Route, on_delete=models.CASCADE)
    # Estimated minutes until the arrival of the vehicle.
    arrival_minutes = models.IntegerField()
    # Timestamp when this predicition was created.
    generated_at = models.DateTimeField(auto_now_add=True)
