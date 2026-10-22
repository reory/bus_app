from django.contrib import admin

from .models import Route, Stop, StopTime, Trip

admin.site.register(Route)
admin.site.register(Stop)
admin.site.register(Trip)
admin.site.register(StopTime)