FROM python:2.7-alpine

# Store required packages for virtual environment 
RUN pip install virtualenv && adduser -D bookcamel 
# Get postgresql dependencies
RUN apk update && \
    apk add --virtual build-deps gcc python-dev musl-dev && \
    apk add postgresql-dev

USER bookcamel
WORKDIR /home/bookcamel

COPY reqs.txt .
COPY cfg.py .
COPY cmd.py .
COPY app app

# Create and populate virtual environment
RUN virtualenv --python=python2.7 nv && source nv/bin/activate \
 && pip install -r reqs.txt

EXPOSE 8000 

ENTRYPOINT source nv/bin/activate \
               && until nc -z postgres 5432; do sleep 1; done \
               && gunicorn --access-logfile access.log --error-logfile errors.log -b :8000 cmd:app

# For debugging
# ENTRYPOINT source nv/bin/activate && ./cmd.py runserver -h 0.0.0.0 -p 8000 &> out.txt


