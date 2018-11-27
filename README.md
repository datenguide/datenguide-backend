# datenguide-backend

A small [flask](http://flask.pocoo.org/) powered app that exposes an
elasticsearch index into a [GraphQL](https://graphql.org/)-api to make german
public data from *GENESIS*-instances like
[www.regionalstatistik.de](http://www.regionalstatistik.de) accessible for
*computers*.

It is also the backend api that runs behind [datengui.de](https://datengui.de),
to make this data accessible for *humans* then.

It also provides a web frontend to play around with the api:

![graphiql screenshot](img/graphiql.png)

## Live running instance

You could find this app running live at https://api.genesapi.org

## Setup

requires Python 3

    pip install -r requirements.txt

The app relies on an
[Elasticsearch](https://www.elastic.co/products/elasticsearch)-Index to
request data from.

There is a dedicated app that can download data cubes from *GENESIS*-Instances
and load them into an Elasticsearch index: [genesapi-cli](https://github.com/datenguide/genesapi-cli)

## Run Flask app

The flask app has some settings in `settings.py` that can all be set via
environment variables.

Defaults:

```python
SCHEMA = 'data/schema.json'  # path to schema created with `genesapi-pipeline`
NAMES = 'data/names.json'    # path to names created with `genesapi-pipeline`
ELASTIC_HOST = 'localhost'
ELASTIC_PORT = 9200
ELASTIC_INDEX = 'genesapi'
```

for debug mode, run the app locally like this, assuming the names & schema
data is in `./data/` (there is some sample data in this repo):

    FLASK_DEBUG=1 FLASK_APP=app.py flask run

If the data is somewhere else, just add these env vars before:

    NAMES=/path/to/data/names.json SCHEMA=/path/to/data/schema.json FLASK_DEBUG=1 FLASK_APP=app.py flask run

For deployment, set the `DEBUG`-variable to `False`, obviously, and adjust the
other environment variables.

## How to query data

[See documentation here](https://github.com/datenguide/datenguide/blob/master/docs/_api-docs/api_docs.md)
