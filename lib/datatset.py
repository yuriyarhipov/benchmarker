import psycopg2


class DataSet(object):

    def __init__(self):
        self.conn = psycopg2.connect(
            'host = localhost dbname = benchmarker user = postgres password = 1297536'
        )
        cursor = self.conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS datasets (
            project_id INTEGER,
            equipment TEXT,
            module TEXT,
            ms1 TEXT,
            ms2 TEXT,
            ms3 TEXT,
            ms4 TEXT,
            ms5 TEXT,
            ms6 TEXT,
            ms7 TEXT,
            ms8 TEXT,
            ms9 TEXT,
            ms10 TEXT,
            ms11 TEXT,
            ms12 TEXT,
            ms13 TEXT
        );''')
        self.conn.commit()

    def add_row(self, project_id, equipment, module, file_columns, ms):
        cursor = self.conn.cursor()

        columns = ['project_id', 'equipment', 'module', ]
        columns.extend(file_columns)
        values = [project_id, equipment, module]

        for ms_value in ms:
            values.append(ms_value)

        sql_columns = ','.join(columns)
        sql_values = ','.join(["'%s'" % val for val in values])
        cursor.execute('DELETE FROM datasets WHERE (project_id=%s) AND (equipment=%s) AND (module=%s)', (int(project_id), equipment, str(module)))
        cursor.execute('INSERT INTO datasets (%s) VALUES (%s);' % (sql_columns, sql_values))
        self.conn.commit()

    def get_dataset(self, project_id):
        data = dict()
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM datasets LIMIT 0;')
        columns = [desc[0] for desc in cursor.description][1:]
        sql_columns = ','.join(columns)
        cursor.execute("SELECT %s FROM datasets WHERE project_id='%s'" % (sql_columns, project_id, ))
        data['data'] = cursor.fetchall()
        data['columns'] = columns
        return data




