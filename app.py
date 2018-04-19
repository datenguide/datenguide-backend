from flask import Flask, Response
from flask_graphql import GraphQLView

from settings import DEBUG
from schema import schema, query


app = Flask(__name__)
app.debug = DEBUG


if app.debug:
    @app.route('/query/')
    def full_query():
        return Response(query)


app.add_url_rule('/', view_func=GraphQLView.as_view(
    'graphql', schema=schema, graphiql=True)
)
