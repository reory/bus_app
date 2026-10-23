from django.core.management.base import BaseCommand

from api.models import Route as APIRoute
from api.models import Stop as APIStop
from bus_backend.apps.routes.models import Route as GTFSRoute
from bus_backend.apps.routes.models import StopTime, Trip


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
        
        # Iterate through routes, pick one representative trip, and sync its stops in sequence
        for route in GTFSRoute.objects.all():
            first_trip = Trip.objects.filter(route=route).first()
            if not first_trip:
                continue

            route_stop_times = (
                StopTime.objects
                .filter(trip=first_trip)
                .select_related("stop")
                .order_by("stop_sequence")
            )
            
            for st in route_stop_times:
                APIStop.objects.create(
                    # Use GTFS route_id as API ID.
                    stop_id=st.stop.stop_id,
                    # Human readable name.
                    name=st.stop.name,
                    # Link to the correct route.
                    route_id=route.route_id,
                    # Link to the correct stop order of the route.
                    order=st.stop_sequence
                )