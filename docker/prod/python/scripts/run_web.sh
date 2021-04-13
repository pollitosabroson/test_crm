
#!/bin/sh

# wait for PSQL server to start
sleep 10

su -m myuser -c "python manage.py makemigrations"
su -m myuser -c "python manage.py migrate"
su -m myuser -c "python manage.py collectstatic --link --no-input"
su -m myuser -c "gunicorn --bind 0.0.0.0:5560 api.wsgi"
