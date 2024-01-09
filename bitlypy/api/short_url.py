from flask import Blueprint, g, jsonify, request
from flask import current_app as app
from urllib.parse import unquote
from pydantic import BaseModel, HttpUrl
from result import Err, Ok

from ..errors import SHORT_ID_ALREADY_EXIST, SHORT_URL_NOT_FOUND
from ..services.short_url import delete_short_url, shorten_url, find_original_url
from .auth import auth_required

bp = Blueprint("short_url", __name__, url_prefix="/short_url")


class CreateShortUrlInput(BaseModel):
    url: HttpUrl


class DeleteShortUrlInput(BaseModel):
    short_url: HttpUrl


@bp.route("", methods=["POST"])
@auth_required
def create():
    """Create and save a new short url."""
    user_id = g.user_id
    create_input = CreateShortUrlInput(**request.get_json())

    short_url = shorten_url(create_input.url, user_id)
    match short_url:
        case Ok(short_url):
            return jsonify({"short_url": short_url}), 201
        case Err(err):
            if err == SHORT_ID_ALREADY_EXIST:
                # TODO: return short url in error message
                return f"A short url for {create_input.url} already exist", 409
            app.logger.error(f"Unexpected error while processing create request: {err}")
            return "Internal server error", 500


@bp.route("", methods=["DELETE"])
@auth_required
def delete():
    """Delete a short url"""
    delete_input = DeleteShortUrlInput(**request.get_json())

    original_url = delete_short_url(delete_input.short_url)
    match original_url:
        case Ok(_):
            return "Ok"
            # Would probably be better to return deleted item
            # return jsonify({"original_url": url})
        case Err(err):
            if err == SHORT_URL_NOT_FOUND:
                return "Short url not found", 404
            else:
                app.logger.error(
                    f"Unexpected error while processing delete short url request: {err}"
                )
                return "Internal server error", 500


@bp.route("", methods=["GET"])
def decode():
    """Get original url from short url"""
    short_url = request.args.get("short_url")
    if short_url is None:
        return "short_url query param is missing"
    decoded_short_url = unquote(short_url)

    original_url = find_original_url(HttpUrl(decoded_short_url))
    match original_url:
        case Ok(url):
            return jsonify({"original_url": url})
        case Err(err):
            if err == SHORT_URL_NOT_FOUND:
                return "Short url not found", 404
            else:
                app.logger.error(
                    f"Unexpected error while processing delete short url request: {err}"
                )
                return "Internal server error", 500
