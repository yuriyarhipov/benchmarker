from djcelery import celery

@celery.task
def worker(project=None):
    if not project:
        return