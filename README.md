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

Data is stored in key-value pairs.

[Get `!ID`s for districts to refetch them (following `Relay` spec):](http://127.0.0.1:5000/?query=%7B%0A%20%20districts%20%7B%0A%20%20%20%20id%0A%20%20%7D%0A%7D%0A)

```graphql
{
  districts {
    id
  }
}
```

[Get data (depth: 2) for individual district:](http://127.0.0.1:5000/?query=%7B%0A%20%20node(id%3A%22Data%3A01001%22)%20%7B%0A%20%20%20%20...%20on%20Data%20%7B%0A%20%20%20%20%20%20data%20%7B%0A%20%20%20%20%20%20%20%20key%0A%20%20%20%20%20%20%20%20value%0A%20%20%20%20%20%20%20%20data%20%7B%0A%20%20%20%20%20%20%20%20%20%20key%0A%20%20%20%20%20%20%20%20%20%20value%0A%20%20%20%20%20%20%20%20%7D%0A%20%20%20%20%20%20%7D%0A%20%20%20%20%7D%0A%20%20%7D%0A%7D%0A)

```graphql
{
  node(id:"Data:01001") {
    ... on Data {
      data {
        key
        value
        data {
          key
          value
        }
      }
    }
  }
}
```
