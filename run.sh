export C_FORCE_ROOT="true"
python manage.py celeryd -l info &
gunicorn_django -t 12000 -w 8 --bind benchmarker.yura.cc:8001 &