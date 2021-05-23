import os
from celery import Celery


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'test_tft.settings')

app = Celery('test_tft')

app.config_from_object('django.conf:settings', namespace='CELERY')

# Loadall task modules
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')