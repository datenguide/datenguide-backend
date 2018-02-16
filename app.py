from flask import Flask, render_template, Response
from flask_graphql import GraphQLView

from schema import schema, doc_content, query


app = Flask(__name__)
app.debug = True


if app.debug:
    @app.route('/docs/')
    def docs():
        return render_template('docs.html', doc=doc_content)

    @app.route('/query/')
    def full_query():
        return Response(query)


app.add_url_rule('/', view_func=GraphQLView.as_view(
    'graphql', schema=schema, graphiql=True)
)


if __name__ == '__main__':
    app.run()
