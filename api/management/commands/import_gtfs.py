from django.core.management.base import BaseCommand
from django.conf import settings
import csv
import os

from bus_backend.apps.routes.models import Route, Stop, Trip, StopTime


class Command(BaseCommand):
    help = "Import GTFS data from local folder"

    def handle(self, *args, **kwargs):
        base = settings.GTFS_PATH

        self.import_routes(os.path.join(base, "routes.txt"))
        self.import_stops(os.path.join(base, "stops.txt"))
        self.import_trips(os.path.join(base, "trips.txt"))
        self.import_stop_times(os.path.join(base, "stop_times.txt"))

        self.stdout.write(self.style.SUCCESS("GTFS import complete"))

    def import_routes(self, path):
        with open(path, newline="", encoding="utf-8") as f:
            for row in csv.DictReader(f):
                Route.objects.get_or_create(
                    route_id=row["route_id"],
                    defaults={
                        "short_name": row.get("route_short_name", ""),
                        "long_name": row.get("route_long_name", ""),
                        "route_type": int(row.get("route_type", 3))
                    },
                )

    def import_stops(self, path):
        with open(path, newline="", encoding="utf-8") as f:
            for row in csv.DictReader(f):
                Stop.objects.get_or_create(
                    stop_id=row["stop_id"],
                    defaults={"name": row["stop_name"]},
                )

    def import_trips(self, path):
        with open(path, newline="", encoding="utf-8") as f:
            for row in csv.DictReader(f):
                Trip.objects.get_or_create(
                    trip_id=row["trip_id"],
                    route_id=row["route_id"],
                )

    def import_stop_times(self, path):
        with open(path, newline="", encoding="utf-8") as f:
            for row in csv.DictReader(f):
                StopTime.objects.get_or_create(
                    trip_id=row["trip_id"],
                    stop_id=row["stop_id"],
                    stop_sequence=int(row["stop_sequence"]),
                )
