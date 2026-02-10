# These serializers convert database objects into clean JSON responses for
# Kivy to interpret.

# Convert data into JSON friendly formats.
from rest_framework import serializers
# Import all the database models this API will expose.
from .models import Route, Stop, Alert


class RouteSerializer(serializers.ModelSerializer):

    text = serializers.CharField(source="short_name")

    class Meta:
        # The model this serializer represents.
        model = Route
        # Only expose the route ID and the text to the front end.
        fields = ["route_id", "text", "short_name", "long_name"]

class StopSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stop
        fields = ["stop_id", "name"]

class AlertSerializer(serializers.ModelSerializer):

    title = serializers.SerializerMethodField()
    description = serializers.CharField(source="message")
    severity = serializers.SerializerMethodField()

    class Meta:
        model = Alert
        fields = ["title", "description", "severity"]

    def get_title(self, obj):
        return "Service Alert"
    
    def get_severity(self, obj):
        return "info"