from django.urls import path
from .views import RouteListView, StopListView

urlpatterns = [
    # Endpoints for listing routes and stops.
    path("routes/", RouteListView.as_view()),
    path("stops/", StopListView.as_view()),
]