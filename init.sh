#python /usr/src/app/manage.py collectstatic
python /usr/src/app/manage.py makemigrations
python /usr/src/app/manage.py migrate
python /usr/src/app/manage.py runserver 0.0.0.0:80
#uwsgi --ini /usr/src/app/uwsgi.ini