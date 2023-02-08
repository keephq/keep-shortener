from http import HTTPStatus

import os, sys
print(os.getcwd())
sys.path.insert(0, os.getcwd())

import pytest
from fastapi.testclient import TestClient

from app.core import config
from app.main import app

client = TestClient(app)


@pytest.fixture(scope="module")
def api_token():
    # Get token.
    return ""


def test_post_short_url():
    """Should return 401."""

    # Unauthorized request.
    response = client.post("/s")
    assert response.status_code == HTTPStatus.UNAUTHORIZED


def test_url_not_exists(api_token):
    """Should return 404."""

    # Authorized but should raise 400 error.
    response = client.get(
        "/api_a/a",
        headers={
            "Accept": "application/json",
            "Authorization": api_token,
        },
    )
    assert response.status_code == HTTPStatus.NOT_FOUND
