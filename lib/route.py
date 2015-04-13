import psycopg2
from os.path import basename

from geopy.distance import vincenty

class Route(object):
    filename = None
    latitude = 'All-Latitude Decimal Degree (Text)'
    longitude = 'All-Longitude Decimal Degree (Text)'

    def __init__(self):
        self.conn = psycopg2.connect(
            'host = localhost dbname = benchmarker user = postgres password = 1297536'
        )

    def create_table(self):
        cursor = self.conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS
            points (project_id TEXT, module TEXT, filename TEXT, time TEXT, ms TEXT, latitude TEXT, longitude TEXT)''' )
        cursor.execute('''DELETE FROM points WHERE filename='%s' ''' % (basename(self.filename)))
        self.conn.commit()

    def parse(self, project_id, module, filename):
        self.filename = filename
        with open(self.filename) as f:
            first_line = f.readline()
            columns = [col for col in first_line.split('\t')]
            idx_latitude = columns.index(self.latitude)
            idx_longitude = columns.index(self.longitude)

            self.create_table()
            sql_filename = basename(self.filename)
            i = 0
            cursor = self.conn.cursor()
            cursor.execute('''DELETE FROM points WHERE (project_id='%s') AND (module='%s') AND (filename='%s') ''' % (project_id, module, sql_filename))
            for row in f:
                row = row.split('\t')
                latitude = row[idx_latitude]
                longitude = row[idx_longitude]
                if (latitude != '') and (longitude != ''):
                    cursor.execute('''INSERT INTO points VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s')''' % (
                        project_id,
                        module,
                        sql_filename,
                        row[0],
                        row[1],
                        latitude,
                        longitude))
                    i += 1
        self.conn.commit()

    def get_points(self, project_id, module, filenames, distance):
        data = []
        cursor = self.conn.cursor()

        sql_filename = ','.join(["'%s'" % basename(f) for f in filenames])
        cursor.execute('''SELECT latitude, longitude FROM points WHERE (project_id='%s') AND (module='%s') AND (filename IN (%s));''' % (project_id, module, sql_filename));
        i = 0
        route_distance = float(0)
        for row in cursor:
            i += 1
            if len(data) == 0:
                data.append(dict(longitude=row[1], latitude=row[0], id=i))
            else:
                last_point = data[-1]

                current_point = dict(longitude=row[1], latitude=row[0], id=i, icon='/static/bul.png')
                current_distance = vincenty((last_point['latitude'], last_point['longitude']), (current_point['latitude'], current_point['longitude'])).meters
                if current_distance > distance:
                    route_distance = route_distance + current_distance
                    data.append(current_point)
        print route_distance
        return data


