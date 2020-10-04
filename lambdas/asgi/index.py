import os

from mangum import Mangum
from quart import Quart

ASGI_BASE_PATH = os.environ.get("asgi_base_path")

app = Quart(__name__)

handler = Mangum(app, api_gateway_base_path=ASGI_BASE_PATH)


@app.route("/")
def hello_world():
    return "Hello, asgi!"
