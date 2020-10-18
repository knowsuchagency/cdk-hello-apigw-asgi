from apig_wsgi import make_lambda_handler
from flask import Flask, request, jsonify

app = Flask(__name__)
app.url_map.strict_slashes = False

handler = make_lambda_handler(app)


@app.route("/wsgi")
def wsgi():
    resp = {"path": request.path}
    return jsonify(resp)


@app.route("/wsgi/foo")
def wsgi_foo():
    resp = {"path": request.path}
    return jsonify(resp)
