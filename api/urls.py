from django.urls import path

# Import the API views.
from .views import(
    RouteListView,
    StopListView,
    PredictionView,
    AlertListView
)

# URL patterns for all API endpoints in this app.
urlpatterns = [
    # Returns all bus routes.
    path("routes/", RouteListView.as_view(), name="route-list"),
    # Returns stops for a specific route.
    path("routes/<str:route_id>/stops/", StopListView.as_view(), name="stop-list"),
    # Returns mocked arrival predictions.
    path(
        "predictions/<str:route_id>/<str:stop_id>/", 
        PredictionView.as_view(), 
        name="prediction"
    ),
    # Returns all alerts.
    path("alerts/", AlertListView.as_view(), name="alert-list"),
]
