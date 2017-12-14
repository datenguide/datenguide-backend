# datenguide-backend

Backend for datenguide application.

Collects datasets and prepares data for `GraphQL`-api.

## Setup

requires Python 3

    pip install -r requirements.txt


## Build data

    python build.py


## Run server

    FLASK_APP=app.py flask run

Visit interactive `GraphiQL` at [http://127.0.0.1:5000/districts](http://127.0.0.1:5000/districts)
