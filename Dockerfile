FROM python:3.9.7-buster

WORKDIR /code
COPY movies_admin/config/requirements/base.txt .
RUN pip3 install --upgrade pip && pip3 install -r base.txt
COPY ./movies_admin .
CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000"]
