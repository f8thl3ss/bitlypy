from os import environ

from data import test_api_key
from flask import Flask
from flask.testing import FlaskClient
from urllib.parse import urlencode
from pydantic import HttpUrl
from sqlalchemy import select
from werkzeug.test import TestResponse

from bitlypy import db
from bitlypy.api.short_url import CreateShortUrlInput, DeleteShortUrlInput
from bitlypy.models import ShortUrl

key = test_api_key["key"]
api_key_headers = {"Authorization": f"apikey {key}", "Content-Type": "application/json"}
ORIGINAL_TEST_URL = "http://google.ca/"
api_url = environ["API_URL"]


def create_test_url(client: FlaskClient) -> TestResponse:
    return client.post(
        "/short_url",
        data=CreateShortUrlInput(url=HttpUrl(ORIGINAL_TEST_URL)).model_dump_json(),
        headers=api_key_headers,
    )


# TODO: test without credentials
def test_create_short_url(client: FlaskClient, app: Flask):
    response = create_test_url(client)
    response_json = response.get_json()
    assert response.status_code == 201
    assert "short_url" in response_json
    assert response_json["short_url"].startswith(f"{api_url}/")

    # test that the user was inserted into the database
    with app.app_context():
        short_url_in_db = db.session.execute(
            select(ShortUrl).filter_by(short_url=response_json["short_url"])
        ).scalar()
        assert short_url_in_db is not None


# TODO: test without credentials
def test_delete_short_url(client: FlaskClient, app: Flask):
    response_json = create_test_url(client).get_json()
    response = client.delete(
        "/short_url",
        data=DeleteShortUrlInput(
            short_url=HttpUrl(response_json["short_url"])
        ).model_dump_json(),
        headers=api_key_headers,
    )
    response_json = response.get_json()
    assert response.status_code == 200

    # test that the user was inserted into the database
    with app.app_context():
        short_url_in_db = db.session.execute(
            select(ShortUrl).filter_by(short_url=ORIGINAL_TEST_URL)
        ).scalar()
        assert short_url_in_db is None


# TODO: test with a short url that doesnt exist
def test_get_original_url(client: FlaskClient):
    response_json = create_test_url(client).get_json()
    params = urlencode({"short_url": response_json["short_url"]})
    response = client.get(
        f"/short_url?{params}",
    )
    response_json = response.get_json()
    assert response.status_code == 200
    assert "original_url" in response_json
    assert response_json["original_url"] == ORIGINAL_TEST_URL
