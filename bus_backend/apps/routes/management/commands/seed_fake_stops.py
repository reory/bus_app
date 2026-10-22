import random
from datetime import time

from django.core.management.base import BaseCommand
from faker import Faker

from bus_backend.apps.routes.models import Route, Stop, StopTime, Trip

fake = Faker()

class Command(BaseCommand):
    help = "Seeds the database with realistic multi-stop routes chained together logically."

    def add_arguments(self, parser):
        parser.add_argument(
            "--count", 
            type=int, 
            default=10, 
            help="Number of fake ROUTES to generate"
        )

    def handle(self, *args, **kwargs):
        count = kwargs["count"]
        real_stops = list(Stop.objects.all())

        if not real_stops:
            self.stdout.write(self.style.ERROR("No real stops found to use as anchors!"))
            return

        # Clear out old fake data to avoid ID conflicts
        self.stdout.write("Cleaning up old fake routes and stops...")

        # Delete StopTimes linked to fake trips
        StopTime.objects.filter(
            trip__trip_id__startswith="T_FAKE_")._raw_delete(using=StopTime.objects.db)
        
        # Delete fake Trips
        Trip.objects.filter(
            trip_id__startswith="T_FAKE_")._raw_delete(using=Trip.objects.db)
        
        # Delete fake Routes
        Route.objects.filter(
            route_id__startswith="R_FAKE_")._raw_delete(using=Route.objects.db)
        
        # Delete fake Stops
        Stop.objects.filter(
            stop_id__startswith="FAKE_")._raw_delete(using=Stop.objects.db)

        self.stdout.write(f"Generating {count} realistic multi-stop routes...")

        for i in range(count):
            # Create a distinct Route
            route_id = f"R_FAKE_{i}"
            route = Route.objects.create(
                route_id=route_id,
                short_name=str(random.randint(100, 999)),
                long_name=f"{fake.city()} Express",
                route_type=3
            )

            # Create a Trip container for the stops
            trip = Trip.objects.create(
                trip_id=f"T_FAKE_{i}",
                route=route,
                headsign="City Centre",
            )

            # Choose a single real stop to anchor this ENTIRE route line
            anchor = random.choice(real_stops)
            current_lat = anchor.lat
            current_lon = anchor.lon

            # Establish a logical "trajectory" vector for this specific bus line
            # This ensures the stops march along a path rather than scattering randomly
            lat_step = random.uniform(-0.0015, 0.0015)
            lon_step = random.uniform(-0.0015, 0.0015)

            # Generate a sequence of 5 to 8 stops along this route line
            stops_per_route = random.randint(5, 8)
            base_hour = random.randint(6, 18)

            for seq in range(1, stops_per_route + 1):
                # Move the coordinate along the vector path with a tiny bit of jitter
                current_lat += lat_step + random.uniform(-0.0003, 0.0003)
                current_lon += lon_step + random.uniform(-0.0003, 0.0003)

                # Create a unique stop along the path
                new_stop = Stop.objects.create(
                    stop_id=f"FAKE_{i}_{seq}_{random.randint(10, 99)}",
                    name=f"{fake.street_name()} & {fake.street_name()}",
                    lat=round(current_lat, 6),
                    lon=round(current_lon, 6)
                )

                # Link the stop to the trip with an incremental sequence number
                StopTime.objects.create(
                    trip=trip,
                    stop=new_stop,
                    stop_sequence=seq,
                    # Increment arrival times logically by 5 minutes per stop
                    arrival_time=time(hour=base_hour, minute=((seq * 5) % 60))
                )

        self.stdout.write(self.style.SUCCESS(f"Successfully generated {count} continuous bus lines!"))