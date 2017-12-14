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

## Query using GraphQL

Visit interactive `GraphiQL` at [http://127.0.0.1:5000/districts](http://127.0.0.1:5000/districts)

List all districts:

```graphql
{
  districts {
    id
    name
    area
  }
}
```

Get data for an individual district:

```graphql
{
  district(id:"01002") {
    id
    name
    area
  }
}
```
