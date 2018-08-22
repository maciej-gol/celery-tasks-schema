from celery import Celery


app = Celery('main')
app.autodiscover_tasks(['test_app.schema'], force=True)
