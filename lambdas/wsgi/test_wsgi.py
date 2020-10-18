import os

import pytest
import requests
from index import app


@pytest.fixture
def url():
    return os.environ["http_api_url"]


@pytest.fixture()
def client():
    with app.test_client() as client_:
        yield client_


def test_wsgi_functional(client):
    resp = client.get("/wsgi")
    assert "path" in resp.json


@pytest.mark.integration
def test_wsgi_integration(url):
    with requests.get(f"{url}/wsgi") as resp:
        assert "path" in resp.json()
