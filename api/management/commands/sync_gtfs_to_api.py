from django.core.management.base import BaseCommand
from bus_backend.apps.routes.models import Route as GTFSRoute, Stop as GTFSStop, Trip, StopTime
from api.models import Route as APIRoute, Stop as APIStop

class Command(BaseCommand):
    help = "Sync GTFS data into the API models."

    def handle(self, *args, **kwargs):
        # Run both sync operations.
        self.sync_routes()
        self.sync_stops()
        # Notify success.
        self.stdout.write(self.style.SUCCESS("GTFS -> API sync complete"))

    def sync_routes(self):

        # Clear exisiting API routes.
        APIRoute.objects.all().delete()

        # Loop through GTFS routes.
        for route in GTFSRoute.objects.all():
            APIRoute.objects.create(
            route_id=route.route_id,
            short_name=route.short_name,
            long_name=route.long_name,
        )

    def sync_stops(self):

        # Clear existing API stops.
        APIStop.objects.all().delete()
        
        processed_routes = set()

        stop_times = (
             StopTime.objects
             .select_related("trip", "stop","trip__route")
             .order_by("trip__route__route_id", "stop_sequence")
        )

        for st in stop_times:
            route_id = st.trip.route.route_id

            # Only process the first trip per route.
            if route_id in processed_routes:
                continue

            APIStop.objects.create(
                # Use GTFS route_id as API ID.
                stop_id=st.stop.stop_id,
                # Human readable name.
                name=st.stop.name,
                # Link to the correct route.
                route_id=route_id,
                # Link to the correct stop order of the route.
                order=st.stop_sequence
            )
            
            processed_routes.add(route_id)