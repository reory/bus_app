from rest_framework import serializers
from .models import Prediction

class PredictionSerializer(serializers.ModelSerializer):
    """Serializer for Prediction model data."""
    class Meta:
        # Use the POrediction model.
        model = Prediction
        # Expose all fields in the API responses.
        fields = "__all__"