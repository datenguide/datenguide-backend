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

List all districts:

```graphql
{
  districts {
    id
    name
  }
}
```

Get data for an individual district (via relay):

```graphql
{
  node(id:"District:01002") {
    ... on District {
      rs
      name
      area
    }
  }
}
```


List all datasets:
```graphql
{
  datasets {
    id
  }
}
```

Get data for an individual dataset (via relay):

```graphql
{
  node(id: "Dataset:21111") {
    ... on Dataset {
      tables
    }
  }
}
```
