from rest_framework import generics
from .models import Route, Stop
from .serializers import RouteSerializer, StopSerializer

class RouteListView(generics.ListAPIView):
    """API endpoint for listing all routes."""

    # Return all route records for this view.
    queryset = Route.objects.all()

    # Use RouteSerializer to format the API output.
    serializer_class = RouteSerializer

class StopListView(generics.ListAPIView):
    """API endpoint for lisiting all stops."""

    # Use StopSerializer to format the API output.
    serializer_class = StopSerializer

    def get_queryset(self):
        """Override to provide custom filtering logic."""
        
        # Read optional route filter from query string.
        route_id = self.request.query_params.get("route_id")

        if route_id:
            # Filter stops by the selected route (avoid duplication)
            return Stop.objects.filter(trip__route__route_id=route_id).distinct()
        # No filter applied - return all the stops.
        return Stop.objects.all()