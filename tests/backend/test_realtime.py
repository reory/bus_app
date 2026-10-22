# Directly import the urls module to sweep its routing definitions into 100% coverage
import bus_backend.apps.realtime.urls  #noqa
import pytest
from bus_backend.apps.realtime.models import Prediction
from bus_backend.apps.realtime.views import get_predictions
from bus_backend.apps.routes.models import Route, Stop
from rest_framework.test import APIRequestFactory


@pytest.mark.django_db
def test_get_predictions_no_data():
    """Test branch where no matching predictions exist in the database."""

    factory = APIRequestFactory()
    request = factory.get('/prediction/')
    
    response = get_predictions(request)
    
    assert response.status_code == 200
    assert response.data == {"message": "No prediction available"}


@pytest.mark.django_db
def test_get_predictions_all_unfiltered():
    """Test fetching predictions without applying any query parameters."""

    route = Route.objects.create(
        route_id="R10", short_name="10", long_name="Route 10", route_type=3
    )
    stop = Stop.objects.create(stop_id="S10", name="Stop 10", lat=40.0, lon=-74.0)
    Prediction.objects.create(stop=stop, route=route, arrival_minutes=5)

    factory = APIRequestFactory()
    request = factory.get('/prediction/')
    
    response = get_predictions(request)
    
    assert response.status_code == 200
    assert response.data["arrival_minutes"] == 5


@pytest.mark.django_db
def test_get_predictions_filter_by_stop():
    """Test filtering predictions down by a specific stop_id query parameter."""

    route = Route.objects.create(
        route_id="R10", short_name="10", long_name="Route 10", route_type=3
    )
    stop1 = Stop.objects.create(stop_id="S10", name="Stop 10", lat=40.0, lon=-74.0)
    stop2 = Stop.objects.create(stop_id="S20", name="Stop 20", lat=40.1, lon=-74.1)
    
    Prediction.objects.create(stop=stop1, route=route, arrival_minutes=5)
    Prediction.objects.create(stop=stop2, route=route, arrival_minutes=12)

    factory = APIRequestFactory()
    request = factory.get('/prediction/', {'stop_id': 'S20'})
    
    response = get_predictions(request)
    
    assert response.status_code == 200
    assert response.data["arrival_minutes"] == 12


@pytest.mark.django_db
def test_get_predictions_filter_by_route():
    """Test filtering predictions down by a specific route_id query parameter."""

    route1 = Route.objects.create(
        route_id="R10", short_name="10", long_name="Route 10", route_type=3
    )
    route2 = Route.objects.create(
        route_id="R20", short_name="20", long_name="Route 20", route_type=3
    )
    stop = Stop.objects.create(stop_id="S10", name="Stop 10", lat=40.0, lon=-74.0)
    
    Prediction.objects.create(stop=stop, route=route1, arrival_minutes=5)
    Prediction.objects.create(stop=stop, route=route2, arrival_minutes=8)

    factory = APIRequestFactory()
    request = factory.get('/prediction/', {'route_id': 'R20'})
    
    response = get_predictions(request)
    
    assert response.status_code == 200
    assert response.data["arrival_minutes"] == 8