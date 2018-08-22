from celery_app import app


@app.task
def test(b, c, d, e=None):
    pass


@app.task
def test_new(a, b):
    pass
