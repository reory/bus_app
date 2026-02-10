from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# Set default Django settings.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bus_backend.settings")

app = Celery("bus_backend")

# Load config from Django settings, using CELERY_ prefix.
app.config_from_object("django.conf:settings", namespace="CELERY")

# Auto discover tasks in installed apps.
app.autodiscover_tasks()

# Load standalone tasks
@app.on_after_finalize.connect() #type:ignore
def load_standalone_tasks(sender, **kwargs):
    import tasks.gtfs_tasks
    import tasks.cleanup_tasks
    import tasks.realtime_tasks
    import tasks.notifications_tasks
    import tasks.test_tasks