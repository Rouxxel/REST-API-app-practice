from celery import Celery
import logging

# Initialize Celery
def create_celery(app):
    logging.debug("Celery worker set")
    celery = Celery(
        app.import_name,
        backend=app.config['CELERY_RESULT_BACKEND'],
        broker=app.config['CELERY_BROKER_URL']
    )
    celery.conf.update(app.config)
    return celery
