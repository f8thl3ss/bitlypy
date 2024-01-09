from os import environ

from pydantic import HttpUrl
from result import Err, Ok, Result
from sqids.sqids import Sqids

from bitlypy.errors import SHORT_URL_NOT_FOUND

from ..repositories.short_url import delete, find, save

sqids = Sqids()
api_url = environ["API_URL"]


def shorten_url(original_url: HttpUrl, user_id: str) -> Result[str, str]:
    short_id = _generate_short_id(original_url, user_id)
    short_url = _build_short_url(short_id)

    # TODO: Implement a retry strategy for id collisions
    short_url = save(short_url, user_id, original_url.unicode_string())
    match short_url:
        case Ok(url):
            return Ok(url)
        case Err(_):
            return short_url


def delete_short_url(short_url: HttpUrl) -> Result[str, str]:
    return delete(short_url.unicode_string())


def find_original_url(short_url: HttpUrl) -> Result[str, str]:
    short_url_result = find(short_url.unicode_string())
    match short_url_result:
        case Ok(url):
            return Ok(url.original_url)
        case Err(_):
            return Err(SHORT_URL_NOT_FOUND)


def _generate_short_id(url: HttpUrl, user_id: str) -> str:
    return sqids.encode(list(f"{url.unicode_string()}{user_id}".encode()))[0:10]


def _build_short_url(short_id: str) -> str:
    return f"{api_url}/{short_id}"
