from django.db import models

class Route(models.Model):
    """
    Stores key identifiers and metadata so trips and realtime data
    can be linked back to the correct route.
    """
    # unique GTFS identifer for this route.
    route_id = models.CharField(max_length=50, unique=True)
    # Public facing short code - "12", "vb3", etc
    short_name = models.CharField(max_length=20)
    # Full descriptive name of the route.
    long_name = models.CharField(max_length=200)
    # Optional extra info from the GTFS feed.
    description = models.TextField(blank=True)
    #GTFS route categories - bus, train, tram, etc.
    route_type = models.IntegerField()

    def __str__(self):
        """Human readable route name for admin and debugging."""

        return f"{self.short_name} - {self.long_name}"
    

class Stop(models.Model):
    """Represents a physical bus stop from the GTFS feed."""

    # Unique GTFS ID for the stop.
    stop_id = models.CharField(max_length=50, unique=True)
    # Human readable stop name.
    name = models.CharField(max_length=200)
    # Latitude coordinates of the bus stop.
    lat = models.FloatField()
    # Longitude coordiantes of the bus stop.
    lon = models.FloatField()

    def __str__(self):
        """Display the stop name in admin and logs."""

        return self.name
    
        
class Trip(models.Model):
    """Represents a scheduled journey in the GTFS feed."""
    
    # Unique trip ID for the trip.
    trip_id = models.CharField(max_length=50, unique=True)
    # The route this trip belongs to.
    route = models.ForeignKey(Route, on_delete=models.CASCADE)
    # Direction or destination shown to passengers.
    headsign = models.CharField(max_length=200)

    def __str__(self):
        """Show route and directions for easy identification."""
        
        return f"{self.route.short_name} -> {self.headsign}"
    
    
class StopTime(models.Model):
    """Links stops to trips in teh correct sequence from the GTFS feed."""
    
    # Trip this stop belongs to.
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE)
    # Stop reference.
    stop = models.ForeignKey(Stop, on_delete=models.CASCADE)
    # Order within the trip.
    stop_sequence = models.IntegerField()
    # Scheduled/estimated time of the bus arrival.
    arrival_time = models.TimeField()

    class Meta:
        # Ensures correct stop order.
        ordering = ["stop_sequence"]

    def __str__(self):
        """Readable representation for admin and debugging."""

        # Trip + Stop + Sequence summary.
        return f"{self.trip.trip_id} @ {self.stop.name} ({self.stop_sequence})"