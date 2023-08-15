FROM python:3.7.13-alpine3.16
ADD . /app
WORKDIR /app
RUN pip install -r requirements.txt
CMD ["gunicorn"  , "-b", "0.0.0.0", "wsgi:app", "-w", "4"]
EXPOSE 8000