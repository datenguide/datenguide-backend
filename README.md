# datenguide-backend

Backend for datenguide application.

Collects datasets and prepares data for `GraphQL`-api.

## Live running instance

You could find this app running live at https://api.datengui.de

[See below](#how-to-query-data) how to use this `GraphQL`-api.

And [see here](#how-to-query-keys-info) how to query infos about the keys.

## Setup

requires Python 3

    pip install -r requirements.txt


## Build data

    python build.py

This could take some time, depending on how many data you want to load in.

## Run server locally

for debug mode, run the app locally like this:

    FLASK_DEBUG=1 FLASK_APP=app.py flask run

In debug mode, the endpoint `/query/` is available to obtain the full query
syntax for all available fields: http://127.0.0.1:5000/query/

For deployment, set the `DEBUG`-variable to `False`, obviously.

## How to query data

Visit interactive `GraphiQL` at [api.datengui.de](https://api.datengui.de/)

The data is modelled in a tree-ish nested structure and so is the querying via
`GraphQL`.

Data is stored in nested key-value pairs.

### list endpoint

[List all regions (currently german states and districts)](https://api.datengui.de/?query=%7B%0A%20%20regions%20%7B%0A%20%20%20%20id%0A%20%20%20%20name%0A%20%20%7D%0A%7D%0A)

```graphql
{
  regions {
    id
    name
  }
}
```

#### arguments

To filter this list of regions, currently 4 filter arguments are implemented:
- nuts: filter by [nuts level](https://en.wikipedia.org/wiki/Nomenclature_of_Territorial_Units_for_Statistics)
- parent: filter by regions from this parent id
- deprecated: `true` for regions that are not valid anymore (because of
  "Kreisgebietsreformen")
- valid: `not deprecated`

[List all german states](https://api.datengui.de/?query=%7B%0A%20%20regions(nuts%3A%201)%20%7B%0A%20%20%20%20id%0A%20%20%20%20name%0A%20%20%7D%0A%7D%0A)

```graphql
{
  regions(nuts: 1) {
    id
    name
  }
}
```

[List all districts in North-Rhine Westphalia that are not deprecated](https://api.datengui.de/?query=%7B%0A%20%20regions(parent%3A%20%2205%22%2C%20nuts%3A%203%2C%20deprecated%3A%20false)%20%7B%0A%20%20%20%20id%0A%20%20%20%20name%0A%20%20%7D%0A%7D%0A)

```graphql
{
  regions(parent: "05", nuts: 3, valid: true) {
    id
    name
  }
}
```


### detail endpoint

[Query a specific city and show recent numbers for inhabitants](https://api.datengui.de/?query=%7B%0A%20%20region(id%3A%2205911%22)%20%7B%0A%20%20%20%20id%0A%20%20%20%20name%0A%20%20%20%20BEVSTD%20%7B%0A%20%20%20%20%20%20GESM%0A%20%20%20%20%20%20GEST%0A%20%20%20%20%20%20GESW%0A%20%20%20%20%7D%0A%20%20%7D%0A%7D%0A)

```graphql
{
  region(id:"05911") {
    id
    name
    BEVSTD {
      GESM
      GEST
      GESW
    }
  }
}
```

As you see with the example above, the original attributes ("Merkmal") from the
GENESIS-Databases are used.

#### arguments

To get a specific region by `id` (Regionalschlüssel), use the `id`-argument:

[Show the number of female baby cows in Schleswig Holstein for the year 2009](https://api.datengui.de/?query=%7B%0A%20%20region(id%3A%20%2201%22)%20%7B%0A%20%20%20%20id%0A%20%20%20%20name%0A%20%20%20%20TIE003%20%7B%0A%20%20%20%20%20%20TIEA05%20%7B%0A%20%20%20%20%20%20%20%20TIERART204141RW(year%3A%222009%22)%0A%20%20%20%20%20%20%7D%0A%20%20%20%20%7D%0A%20%20%7D%0A%7D%0A)

```graphql
{
  region(id: "01") {
    id
    name
    TIE003 {
      TIEA05 {
        TIERART204141RW(year: "2009")
      }
    }
  }
}
```

[You can query for more than one year by using aliases:](https://api.datengui.de/?query=%7B%0A%20%20region(id%3A%20%2201%22)%20%7B%0A%20%20%20%20id%0A%20%20%20%20name%0A%20%20%20%20TIE003%20%7B%0A%20%20%20%20%20%20TIEA05%20%7B%0A%20%20%20%20%20%20%20%20cows_2009%3A%20TIERART204141RW(year%3A%20%222009%22)%0A%20%20%20%20%20%20%20%20cows_2010%3A%20TIERART204141RW(year%3A%20%222010%22)%0A%20%20%20%20%20%20%7D%0A%20%20%20%20%7D%0A%20%20%7D%0A%7D%0A)

```graphql
{
  region(id: "01") {
    id
    name
    TIE003 {
      TIEA05 {
        cows_2009: TIERART204141RW(year: "2009")
        cows_2010: TIERART204141RW(year: "2010")
      }
    }
  }
}
```

[And of course you can query this for all regions via the **list endpoint** as well:](https://api.datengui.de/?query=%7B%0A%20%20regions%20%7B%0A%20%20%20%20id%0A%20%20%20%20name%0A%20%20%20%20TIE003%20%7B%0A%20%20%20%20%20%20TIEA05%20%7B%0A%20%20%20%20%20%20%20%20cows_2009%3A%20TIERART204141RW(year%3A%20%222009%22)%0A%20%20%20%20%20%20%20%20cows_2010%3A%20TIERART204141RW(year%3A%20%222010%22)%0A%20%20%20%20%20%20%7D%0A%20%20%20%20%7D%0A%20%20%7D%0A%7D%0A)

```graphql
{
  regions {
    id
    name
    TIE003 {
      TIEA05 {
        cows_2009: TIERART204141RW(year: "2009")
        cows_2010: TIERART204141RW(year: "2010")
      }
    }
  }
}
```

### time based data

For fields that contain time-based data for years, you could query for this
field by appending the `__years`-suffix to the field name you want to look up:

If you don't append the `__years`-suffix, the most recent value will be
returned.

[Show the number of people naturalized (in total and with origin from african continent) from 2011-2016](https://api.datengui.de/?query=%7B%0A%20%20regions%20%7B%0A%20%20%20%20id%0A%20%20%20%20name%0A%20%20%20%20BEV008%20%7B%0A%20%20%20%20%20%20STAKNW%20%7B%0A%20%20%20%20%20%20%20%20INSGESAMT__years%20%7B%0A%20%20%20%20%20%20%20%20%20%20_2016%0A%20%20%20%20%20%20%20%20%20%20_2015%0A%20%20%20%20%20%20%20%20%20%20_2014%0A%20%20%20%20%20%20%20%20%20%20_2013%0A%20%20%20%20%20%20%20%20%20%20_2012%0A%20%20%20%20%20%20%20%20%20%20_2011%0A%20%20%20%20%20%20%20%20%7D%0A%20%20%20%20%20%20%20%20ST1__years%20%7B%0A%20%20%20%20%20%20%20%20%20%20_2016%0A%20%20%20%20%20%20%20%20%20%20_2015%0A%20%20%20%20%20%20%20%20%20%20_2014%0A%20%20%20%20%20%20%20%20%20%20_2013%0A%20%20%20%20%20%20%20%20%20%20_2012%0A%20%20%20%20%20%20%20%20%20%20_2011%0A%20%20%20%20%20%20%20%20%7D%0A%20%20%20%20%20%20%7D%0A%20%20%20%20%7D%0A%20%20%7D%0A%7D%0A)

```graphql
{
  regions {
    id
    name
    BEV008 {
      STAKNW {
        INSGESAMT__years {
          _2016
          _2015
          _2014
          _2013
          _2012
          _2011
        }
        ST1__years {
          _2016
          _2015
          _2014
          _2013
          _2012
          _2011
        }
      }
    }
  }
}
```

## How to query keys info

To obtain human-readable information about the used keys, use the `key` or
`keys` endpoints. They provide the following properties:
- `id`
- `name`
- `description`

[all keys](https://api.datengui.de/?query=%7B%0A%20%20keys%20%7B%0A%20%20%20%20id%0A%20%20%20%20name%0A%20%20%7D%0A%7D)

```graphql
{
  keys {
    id
    name
  }
}
```

[the key about number of beds in hospitals](https://api.datengui.de/?query=%7B%0A%20%20key(id%3A%22GES017%22)%20%7B%0A%20%20%20%20id%0A%20%20%20%20name%0A%20%20%20%20description%0A%20%20%7D%0A%7D)

```graphql
{
  key(id:"GES017") {
    id
    name
    description
  }
}
```
