from django.db import connection


class Datasets(object):

    def __init__(self):
        self.conn = connection

    def create_dataset_from_template(self, dataset_name, filename):
        pass




