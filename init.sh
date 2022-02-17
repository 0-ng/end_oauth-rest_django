python /usr/src/app/manage.py collectstatic
python /usr/src/app/manage.py makemigrations
python /usr/src/app/manage.py migrate
nohup python /usr/src/app/manage.py runserver 0.0.0.0:8000 &
uwsgi --ini /usr/src/app/uwsgi.ini