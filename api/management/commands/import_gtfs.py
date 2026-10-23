import csv
import zipfile
from datetime import time

from django.conf import settings
from django.core.management.base import BaseCommand

from bus_backend.apps.routes.models import Route, Stop, StopTime, Trip


class Command(BaseCommand):
    help = "Import GTFS data from a zip archive"

    def handle(self, *args, **kwargs):
        zip_path = settings.GTFS_PATH

        if not zipfile.is_zipfile(zip_path):
            self.stdout.write(self.style.ERROR(f"GTFS path is not a valid zip file: {zip_path}"))
            return

        with zipfile.ZipFile(zip_path, "r") as zf:
            self.import_routes(zf)
            self.import_stops(zf)
            self.import_trips(zf)
            self.import_stop_times(zf)

        self.stdout.write(self.style.SUCCESS("GTFS import complete"))

    def import_routes(self, zf):
        with zf.open("routes.txt") as f:
            reader = csv.DictReader(f.read().decode("utf-8").splitlines())
            for row in reader:
                Route.objects.get_or_create(
                    route_id=row["route_id"],
                    defaults={
                        "short_name": row.get("route_short_name", ""),
                        "long_name": row.get("route_long_name", ""),
                        "route_type": int(row.get("route_type", 3)),
                    },
                )

    def import_stops(self, zf):
        with zf.open("stops.txt") as f:
            reader = csv.DictReader(f.read().decode("utf-8").splitlines())
            for row in reader:
                Stop.objects.get_or_create(
                    stop_id=row["stop_id"],
                    defaults={
                        "name": row["stop_name"],
                        "lat": float(row["stop_lat"]),
                        "lon": float(row["stop_lon"]),
                    },
                )

    def import_trips(self, zf):
        with zf.open("trips.txt") as f:
            reader = csv.DictReader(f.read().decode("utf-8").splitlines())
            for row in reader:
                route = Route.objects.get(route_id=row["route_id"])
                Trip.objects.get_or_create(
                    trip_id=row["trip_id"],
                    defaults={
                        "route": route,
                        "headsign": row.get("trip_headsign", route.long_name),
                    },
                )

    def import_stop_times(self, zf):
        with zf.open("stop_times.txt") as f:
            reader = csv.DictReader(f.read().decode("utf-8").splitlines())
            for row in reader:
                trip = Trip.objects.get(trip_id=row["trip_id"])
                stop = Stop.objects.get(stop_id=row["stop_id"])
                
                # Parse arrival time string (handling standard GTFS time format HH:MM:SS)
                time_str = row["arrival_time"]
                parts = time_str.split(":")
                hour = int(parts[0]) % 24
                minute = int(parts[1])
                second = int(parts[2]) if len(parts) > 2 else 0
                arrival_time = time(hour=hour, minute=minute, second=second)

                StopTime.objects.get_or_create(
                    trip=trip,
                    stop=stop,
                    stop_sequence=int(row["stop_sequence"]),
                    defaults={"arrival_time": arrival_time},
                )