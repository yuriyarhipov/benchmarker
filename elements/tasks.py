from djcelery import celery
from routes.route import StandartRoute

@celery.task
def upload_file(filename, project_id, module):
    StandartRoute([]).save_points_to_database(filename, project_id, module)




