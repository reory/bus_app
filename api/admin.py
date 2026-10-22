from django.contrib import admin

from .models import Alert, Route, Stop

admin.site.register(Route)
admin.site.register(Stop)
admin.site.register(Alert)


