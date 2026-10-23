# These serializers convert database objects into clean JSON responses for
# Kivy to interpret.


from rest_framework import serializers

from bus_backend.apps.users.models import UserFavourite

from .models import Alert, Route, Stop


class RouteSerializer(serializers.ModelSerializer):

    text = serializers.CharField(source="short_name")

    class Meta:
        # The model this serializer represents.
        model = Route
        # Only expose the route ID and the text to the front end.
        fields = ("route_id", "text", "short_name", "long_name")

class StopSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stop
        fields = ("stop_id", "name")

class AlertSerializer(serializers.ModelSerializer):

    title = serializers.SerializerMethodField()
    description = serializers.CharField(source="message")
    severity = serializers.SerializerMethodField()

    class Meta:
        model = Alert
        fields = ("title", "description", "severity")

    def get_title(self, obj):
        return "Service Alert"
    
    def get_severity(self, obj):
        return "info"

class UserFavouriteSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserFavourite
        fields = ("id", "stop_id", "route_id", "nickname", "created_at")