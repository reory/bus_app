from django.contrib import admin
from .models import Route, Stop, Alert

admin.site.register(Route)
admin.site.register(Stop)
admin.site.register(Alert)


