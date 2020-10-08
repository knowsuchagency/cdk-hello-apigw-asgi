from apig_wsgi import make_lambda_handler
from flask import Flask

app = Flask(__name__)
app.url_map.strict_slashes = False

handler = make_lambda_handler(app)


@app.route("/")
def hello_world():
    return "hello, index!"


@app.route("/wsgi")
def wsgi():
    return "hello, wsgi!"


@app.route("/wsgi/foo")
def wsgi_foo():
    return {"hello": "wsgi foo"}
