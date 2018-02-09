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

[Example Query for districts](http://127.0.0.1:5000/?query=%7B%0A%20%20districts%20%7B%0A%20%20%20%20id%0A%20%20%20%20name%0A%20%20%20%20name_ext%0A%20%20%20%20slug%0A%20%20%20%20lat%0A%20%20%20%20lon%0A%20%20%20%20flc006%0A%20%20%20%20bevstd%20%7B%0A%20%20%20%20%20%20gesm%0A%20%20%20%20%20%20gesw%0A%20%20%20%20%20%20t%0A%20%20%20%20%7D%0A%20%20%20%20Schulstatistik%20%7B%0A%20%20%20%20%20%20Gymnasien%20%7B%0A%20%20%20%20%20%20%20%20BIL003%20%7B%0A%20%20%20%20%20%20%20%20%20%20BILKL2%20%7B%0A%20%20%20%20%20%20%20%20%20%20%20%20JGSTUFE11%0A%20%20%20%20%20%20%20%20%20%20%20%20JGSTUFE7%0A%20%20%20%20%20%20%20%20%20%20%7D%0A%20%20%20%20%20%20%20%20%7D%0A%20%20%20%20%20%20%7D%0A%20%20%20%20%7D%0A%20%20%7D%0A%7D%0A)

```graphql
{
  districts {
    id
    name
    name_ext
    slug
    lat
    lon
    flc006
    bevstd {
      gesm
      gesw
      t
    }
    Schulstatistik {
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
    "districts": [
      {
       "id": "01001",
        "name": "Flensburg",
        "name_ext": "Kreisfreie Stadt",
        "slug": "flensburg",
        "lat": "54.783",
        "lon": "9.433",
        "flc006": "56,74",
        "bevstd": {
          "gesm": "42767",
          "gesw": "43175",
          "t": "85942"
        },
        "Schulstatistik": {
          "Gymnasien": {
            "BIL003": {
              "BILKL2": {
                "JGSTUFE11": "445",
                "JGSTUFE7": "363"
              }
            }
          }
        }
      },
      // more districts...
    ]
  }
}
```
