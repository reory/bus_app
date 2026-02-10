import zipfile
import csv
from celery import shared_task
from django.db import transaction
from bus_backend.apps.routes.models import Route, Stop, Trip, StopTime
from api.models import Route as ApiRoute, Stop as ApiStop


@shared_task
def import_gtfs_static(zip_path):
    """Load GTFS static data from a zip file into the database."""

    with zipfile.ZipFile(zip_path, "r") as zf:

        
        # ROUTES
        with zf.open("routes.txt") as f:
            reader = csv.DictReader(f.read().decode("utf-8").splitlines())
            for row in reader:
                Route.objects.update_or_create(
                    route_id=row["route_id"],
                    defaults={
                        "short_name": row["route_short_name"],
                        "long_name": row["route_long_name"],
                        "description": row.get("route_desc", ""),
                        "route_type": int(row["route_type"]),
                    },
                )

        # Build route lookup
        routes = {r.route_id: r for r in Route.objects.all()}

        
        # STOPS
        with zf.open("stops.txt") as f:
            reader = csv.DictReader(f.read().decode("utf-8").splitlines())
            for row in reader:
                Stop.objects.update_or_create(
                    stop_id=row["stop_id"],
                    defaults={
                        "name": row["stop_name"],
                        "lat": float(row["stop_lat"]),
                        "lon": float(row["stop_lon"]),
                    },
                )

        # Build stop lookup
        stops = {s.stop_id: s for s in Stop.objects.all()}


        # TRIPS
        with zf.open("trips.txt") as f:
            reader = csv.DictReader(f.read().decode("utf-8").splitlines())
            for row in reader:
                Trip.objects.update_or_create(
                    trip_id=row["trip_id"],
                    defaults={
                        "route": routes[row["route_id"]],
                        "headsign": row.get("trip_headsign", ""),
                    },
                )

        # Build trip lookup
        trips = {t.trip_id: t for t in Trip.objects.all()}

        # STOP TIMES
        stop_times = []

        with zf.open("stop_times.txt") as f:
            reader = csv.DictReader(f.read().decode("utf-8").splitlines())

            for row in reader:
                stop_times.append(
                    StopTime(
                        trip=trips[row["trip_id"]],
                        stop=stops[row["stop_id"]],
                        stop_sequence=int(row["stop_sequence"]),
                        arrival_time=row["arrival_time"],
                    )
                )

        # Bulk insert once
        with transaction.atomic():
            StopTime.objects.bulk_create(stop_times, ignore_conflicts=True)

    return "GTFS static import completed"


@shared_task
def project_gtfs_to_api(limit_stops=50):
    """
    Project GTFS truth models into simplified API models
    for UI consumption (Kivy).
    """

    gtfs_route = Route.objects.first()
    if not gtfs_route:
        return "No GTFS routes found"

    api_route, _ = ApiRoute.objects.get_or_create(
        route_id=gtfs_route.route_id,
        defaults={
            "short_name": gtfs_route.short_name,
            "long_name": gtfs_route.long_name,
        },
    )

    trip = Trip.objects.filter(route=gtfs_route).first()
    if not trip:
        return "No trips found for route"

    stop_times = (
        StopTime.objects
        .filter(trip=trip)
        .select_related("stop")
        .order_by("stop_sequence")[:limit_stops]
    )

    ApiStop.objects.filter(route=api_route).delete()

    for idx, st in enumerate(stop_times):
        ApiStop.objects.create(
            stop_id=st.stop.stop_id,
            route=api_route,
            name=st.stop.name,
            order=idx,
        )

    return f"Projected {len(stop_times)} stops to API"

