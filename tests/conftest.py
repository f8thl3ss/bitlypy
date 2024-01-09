import os
import tempfile
from collections.abc import Generator

import pytest
from flask import Flask
from flask.testing import FlaskClient

from bitlypy import create_app
from bitlypy.database import db
from tests.data import insert_test_data


@pytest.fixture
def app() -> Generator[Flask, None, None]:
    """Create and configure a new app instance for each test."""
    # create a temporary file to isolate the database for each test
    db_fd, db_path = tempfile.mkstemp()
    # create the app with common test config
    app = create_app({"TESTING": True, "DATABASE": db_path})

    with app.app_context():
        insert_test_data(db.session)
    yield app

    # close and remove the temporary database
    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture
def client(app: Flask) -> FlaskClient:
    """A test client for the app."""
    return app.test_client()


@pytest.fixture
def runner(app):
    """A test runner for the app's Click commands."""
    return app.test_cli_runner()
