import psycopg2
from os.path import basename

class Route(object):
    filename = None
    latitude = 'All-Latitude Decimal Degree (Text)'
    longitude = 'All-Longitude Decimal Degree (Text)'

    def __init__(self, filename):
        self.filename = filename
        self.conn = psycopg2.connect(
            'host = localhost dbname = benchmarker user = postgres password = 1297536'
        )

    def create_table(self):
        cursor = self.conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS points (filename TEXT, time TEXT, ms TEXT, latitude TEXT, longitude TEXT)''' )
        cursor.execute('''DELETE FROM points WHERE filename='%s' ''' % (basename(self.filename)))
        self.conn.commit()

    def parse(self):
        with open(self.filename) as f:
            first_line = f.readline()
            columns = [col for col in first_line.split('\t')]
            idx_latitude = columns.index(self.latitude)
            idx_longitude = columns.index(self.longitude)


            self.create_table()
            sql_filename = basename(self.filename)
            i = 0
            cursor = self.conn.cursor()
            for row in f:
                row = row.split('\t')
                latitude = row[idx_latitude]
                longitude = row[idx_longitude]
                if (latitude != '') and (longitude != ''):
                    cursor.execute('''INSERT INTO points VALUES ('%s', '%s', '%s', '%s', '%s')''' % (sql_filename, row[0], row[1], latitude, longitude))
                    i += 1
        self.conn.commit()

    def get_points(self):
        data = []
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM points;');
        i = 0
        for row in cursor:
            i += 1
            data.append(dict(longitude=row[4], latitude=row[3], id=i))
        return data


