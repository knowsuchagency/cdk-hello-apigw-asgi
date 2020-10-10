from mangum import Mangum
from quart import Quart, request


app = Quart(__name__)
app.url_map.strict_slashes = False

handler = Mangum(app)


@app.route("/")
def hello():
    return {"path": request.path}


@app.route("/asgi")
def hello_asgi():
    return {"path": request.path}


@app.route("/asgi/foo")
def hello_asgi_foo():
    return {"path": request.path}
