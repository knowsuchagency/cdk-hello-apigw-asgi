from apig_wsgi import make_lambda_handler
from flask import Flask, request

app = Flask(__name__)
app.url_map.strict_slashes = False

handler = make_lambda_handler(app)


@app.route("/wsgi")
def wsgi():
    return {"path": request.path}


@app.route("/wsgi/foo")
def wsgi_foo():
    return {"path": request.path}
