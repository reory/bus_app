# Base class for building API endpoints.
from rest_framework.views import APIView
# Standard JSON response wrapper.
from rest_framework.response import Response
# Import the database models.
from .models import Route, Stop, Alert
# Serializers convert models to JSON.
from .serializers import (RouteSerializer, StopSerializer, AlertSerializer)
# Random module to simulate randomness in bus arrival times.
import random
from api.models import Stop as APIStop

"""
API views read from projection models only.
GTFS truth is never queried directly from this layer.
"""

class RouteListView(APIView):
    """Handles GET requests for listing all available bus routes."""

    def get(self, request):

        # Fetch all route records from the database.
        routes = Route.objects.all()
        # Convert the queryset into JSON friendly format.
        serializer = RouteSerializer(routes, many=True)
        # Send JSON back to the frontend (Kivy)
        return Response(serializer.data)
    
class StopListView(APIView):
    """Returns all stops belonging to a specific route."""

    def get(self, request, route_id):

        # Filter stops by the given route ID.
        stops = APIStop.objects.filter(route__route_id=route_id)
        # Serialize the list of stops.
        serializer = StopSerializer(stops, many=True)
        
        # Return JSON back to the frontend.
        return Response(serializer.data)
    
class PredictionView(APIView):
    """Provides arrival predictions for a given route and stop."""

    def get(self, request, route_id, stop_id):
        
        # Base arrival time for the route.
        base_minutes = 3

        # Stable offset per stop (0-5 mins.)
        stop_offset = abs(hash(stop_id)) % 6

        # Small random jitter (0-2 mins)
        jitter = random.randint(0,2)

        minutes = base_minutes + stop_offset + jitter
        next_minutes = minutes + random.randint(5, 8)

        # Gives the illusion 
        # that bus arrival times will vary depending on different stops.
        return Response({
            "arrival_time": f"{minutes} min",
            "next_arrival": f"{next_minutes} min",
            "status": "On time" if minutes < 10 else "Delayed"
        })

class AlertListView(APIView):
    """Returns all active alerts, newest first."""

    def get(self, request):
        # Sort alerts by newest first.
        alerts = Alert.objects.all().order_by("-created_at")
        # Convert alerts to JSON format.
        serializer = AlertSerializer(alerts, many=True)

        # Send JSON to the frontend (Kivy)
        return Response(serializer.data)


