from mangum import Mangum
from quart import Quart


app = Quart(__name__)
app.url_map.strict_slashes = False

handler = Mangum(app)


@app.route("/asgi")
def hello_asgi():
    return {"hello": "asgi"}

@app.route("/asgi/foo")
def hello_asgi_foo():
    return {"hello": "asgi_foo"}
