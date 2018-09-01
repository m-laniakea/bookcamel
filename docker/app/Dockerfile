FROM python:2.7-alpine

# Store required packages for virtual environment 
RUN pip install virtualenv && adduser -D bookcamel 

USER bookcamel
WORKDIR /home/bookcamel

COPY reqs.txt .
COPY cfg.py .
COPY cmd.py .
COPY app app

# Create and populate virtual environment
RUN virtualenv nv && source nv/bin/activate \
 && pip install -r reqs.txt

EXPOSE 8000 

ENTRYPOINT source nv/bin/activate \
               && gunicorn --error-logfile errors.log -b :8000 cmd:app


