from mangum import Mangum
from quart import Quart


app = Quart(__name__)

handler = Mangum(app)


@app.route("/asgi")
def hello_asgi():
    return {"hello": "asgi"}
