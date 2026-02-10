from django.urls import path
from .views import get_predictions

urlpatterns = [
    # Endpoint for fetching arrival predictions.
    path("prediction/", get_predictions),
]