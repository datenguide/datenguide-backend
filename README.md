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

[Get data for individual district:](http://127.0.0.1:5000/?query=%7B%0A%20%20district(id%3A%20%2205911%22)%20%7B%0A%20%20%20%20area%0A%20%20%20%20munis%0A%20%20%20%20name%0A%20%20%20%20pop%20%7B%0A%20%20%20%20%20%20m%0A%20%20%20%20%20%20t%0A%20%20%20%20%20%20w%0A%20%20%20%20%7D%0A%20%20%20%20schulstatistik%20%7B%0A%20%20%20%20%20%20Gymnasien%20%7B%0A%20%20%20%20%20%20%20%20BIL003%20%7B%0A%20%20%20%20%20%20%20%20%20%20BILKL2%20%7B%0A%20%20%20%20%20%20%20%20%20%20%20%20JGSTUFE11%0A%20%20%20%20%20%20%20%20%20%20%20%20JGSTUFE7%0A%20%20%20%20%20%20%20%20%20%20%7D%0A%20%20%20%20%20%20%20%20%7D%0A%20%20%20%20%20%20%7D%0A%20%20%20%20%7D%0A%20%20%7D%0A%7D%0A)

```graphql
{
  district(id: "05911") {
    area
    munis
    name
    pop {
      m
      t
      w
    }
    schulstatistik {
      Gymnasien {
        BIL003 {
          BILKL2 {
            JGSTUFE11
            JGSTUFE7
          }
        }
      }
    }
  }
}

```

should return:
```json
{
  "data": {
    "district": {
      "area": "145,66",
      "munis": "1.0",
      "name": "Bochum, Kreisfreie Stadt",
      "pop": {
        "m": "177427.0",
        "t": "364742.0",
        "w": "187315.0"
      },
      "schulstatistik": {
        "Gymnasien": {
          "BIL003": {
            "BILKL2": {
              "JGSTUFE11": "1263.0",
              "JGSTUFE7": "1110.0"
            }
          }
        }
      }
    }
  }
}
```
