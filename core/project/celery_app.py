import os

from celery import Celery
from celery.schedules import crontab


# Set the default Django settings module for the 'celery' program.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.project.settings.local")

app = Celery("core")

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object("django.conf:settings", namespace="CELERY")

# Load task modules from all registered Django apps.
app.autodiscover_tasks()


app.conf.beat_schedule = {
    "increase-debt-every-3-hours": {
        "task": "core.apps.retail.tasks.increase_debt",
        "schedule": crontab(minute=0, hour="*/3"),
    },
    "decrease-debt-daily-at-630": {
        "task": "core.apps.retail.tasks.decrease_debt",
        "schedule": crontab(minute=30, hour=6),
    },
}
