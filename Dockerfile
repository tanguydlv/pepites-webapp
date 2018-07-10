FROM python:3.6-slim
RUN apt-get -y update
RUN apt-get -y upgrade
RUN apt-get -y install netbase  # Needed by eventlet
RUN apt-get -y install libmagic1 # Needed by python-magic

WORKDIR /app

# Install python deps first
COPY requirements.txt .
RUN pip install -U pip
RUN pip install -r requirements.txt

# Copy sources
COPY ./ .

# Install package
RUN python setup.py install

EXPOSE 8080
ENTRYPOINT flask db upgrade && gunicorn -c gunicorn.py pepites_webapp:app
