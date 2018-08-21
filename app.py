from flask import Flask, request, jsonify
from flask_graphql import GraphQLView

from schema import schema
from elastic import search, suggest, get_fact


app = Flask(__name__)


app.add_url_rule('/', view_func=GraphQLView.as_view(
    'graphql', schema=schema, graphiql=True)
)


@app.route('/search/')
def search_view():
    q = request.args.get('q')
    response = jsonify(search(q))
    if app.debug:
        response.headers.add('Access-Control-Allow-Origin', '*')
    return response


@app.route('/suggest/')
def suggest_view():
    q = request.args.get('q')
    response = jsonify(suggest(q))
    if app.debug:
        response.headers.add('Access-Control-Allow-Origin', '*')
    return response


@app.route('/fact/<fact_id>')
def detail_view(fact_id):
    response = jsonify(get_fact(fact_id))
    if app.debug:
        response.headers.add('Access-Control-Allow-Origin', '*')
    return response
