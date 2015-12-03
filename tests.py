import csv
from geopy.distance import vincenty
from operator import itemgetter


filename = '0610045429.txt'


data = []
with open(filename) as csvfile:
    reader = csv.DictReader(csvfile, delimiter='\t')
    columns = reader.fieldnames
    for column in columns:
        if 'latitude' in column.lower():
            latitude_column = column
        elif 'longitude' in column.lower():
            longitude_column = column
    MS_column = 'MS'
    init_point = None
    for row in reader:
        longitude = row.get(longitude_column).strip()
        latitude = row.get(latitude_column).strip()
        if (longitude != '') and (latitude != ''):
            if longitude != '':
                if not init_point:
                    init_point = [latitude, longitude, ]
                data.append([
                    latitude,
                    longitude,
                ])
print len(data)


def points_sort(data, index_range):
    data.sort()
    status = True
    idx = 1
    while status:
        status = False
        for i in range(len(data)):
            if i + idx < len(data):
                while (i + idx < len(data)) and (vincenty(data[i], data[i + idx]).meters <= 1):
                    data.pop(i + idx)
            else:
                break
        if idx < index_range:
            status = True
            idx += 1
    return data

data = points_sort(data, 10)
