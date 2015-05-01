from django.conf import settings


def handle_uploaded_file(uploaded_files):
    path = settings.STATICFILES_DIRS[0]
    result = []
    for f in uploaded_files:
        filename = '/'.join([path, f.name])
        destination = open(filename, 'wb+')
        for chunk in f.chunks():
            destination.write(chunk)
        destination.close()
        result.append(filename)
    return result