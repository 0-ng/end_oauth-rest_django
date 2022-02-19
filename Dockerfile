FROM python:3.6

RUN python -m pip install -U --force-reinstall pip

WORKDIR /usr/src/app
COPY ./ ./
RUN pip install --no-cache-dir -r /usr/src/app/requirements.txt  -i https://pypi.tuna.tsinghua.edu.cn/simple
EXPOSE 80
#CMD ["uwsgi", "--ini", "uwsgi.ini"]
CMD ["bash", "init.sh"]
#CMD ["python", "manage.py", "runserver"]
