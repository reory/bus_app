# Django RestFramework tool for building API serializers.
from rest_framework import serializers
from .models import Route, Stop, Trip

class RouteSerializer(serializers.ModelSerializer):
    """Serializes Route model for API responses."""
    class Meta:
        # Use the Route model for this serializer.
        model = Route
        # Expose all model fields in the API.
        fields = "__all__"

class StopSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stop
        fields = "__all__"

class TripSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trip
        fields = "__all__"