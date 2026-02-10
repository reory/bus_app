from rest_framework.response import Response
# Marks a function based view as a DRF API endpoint.
from rest_framework.decorators import api_view
from .models import Prediction
from .serializers import PredictionSerializer

@api_view(["GET"])
def get_predictions(request):
    """Function based API endpoint for GET-only fetching arrival predictions."""

    # Stop filter from query string.
    stop_id = request.query_params.get("stop_id")
    # Route filter from query string.
    route_id = request.query_params.get("route_id")
    
    # Start with all predictions.
    qs = Prediction.objects.all()

    if stop_id:
        # Narrow down to predictions for this stop.
        qs = qs.filter(stop__stop_id=stop_id)
    if route_id:
        # Narrow down to predictions for this route.
        qs = qs.filter(route__route_id=route_id)
    
    # Get the most recently generated prediction.
    latest = qs.order_by("-generated_at").first()

    if not latest:
        # No matching prediction found.
        return Response({"message": "No prediction available"})
    
    # Return serialized prediction data.
    return Response(PredictionSerializer(latest).data)