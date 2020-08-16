web: bin/start-nginx gunicorn -c gunicorn.conf {{ project_name }}.wsgi:application
worker: REMAP_SIGTERM=SIGQUIT celery -E  -A {{ project_name }} worker
release: python manage.py migrate
