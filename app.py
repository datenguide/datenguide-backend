from flask import Flask
from flask_graphql import GraphQLView

from schema import districts


app = Flask(__name__)
app.debug = True

app.add_url_rule('/districts', view_func=GraphQLView.as_view(
    'districts', schema=districts, graphiql=True)
)


if __name__ == '__main__':
    app.run()
