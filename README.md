# datenguide-backend

Backend for datenguide application.

Collects datasets and prepares data for `GraphQL`-api.

## Setup

requires Python 3

    pip install -r requirements.txt


## Build data

    python build.py


## Run server

    python app.py

## Query using GraphQL

Visit interactive `GraphiQL` at [http://127.0.0.1:5000/](http://127.0.0.1:5000/)

The data is modelled in a tree-ish nested structure and so is the querying via `GraphQL`.

Data is stored in nested key-value pairs.

[Get list of ids for districts to query later on:](http://127.0.0.1:5000/?query=%7B%0A%20%20districts%0A%7D%0A)

```graphql
{
  districts
}
```

[Get data for individual district:](http://127.0.0.1:5000/?query=%7B%0A%20%20district(id%3A%2201001%22)%20%7B%0A%20%20%20%20area%0A%20%20%20%20name%0A%20%20%20%20munis%0A%20%20%20%20pop%20%7B%0A%20%20%20%20%20%20t%0A%20%20%20%20%20%20m%0A%20%20%20%20%20%20w%0A%20%20%20%20%7D%0A%20%20%7D%0A%7D%0A)

```graphql
{
  district(id:"01001") {
    area
    name
    munis
    pop {
      t
      m
      w
    }
  }
}
```

should return:
```json
{
  "data": {
    "district": {
      "area": "56,74",
      "munis": "1.0",
      "name": "Flensburg, Kreisfreie Stadt",
      "pop": {
        "m": "42767.0",
        "t": "85942.0",
        "w": "43175.0"
      }
    }
  }
}
```
