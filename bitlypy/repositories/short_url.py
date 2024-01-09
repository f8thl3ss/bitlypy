from result import Err, Ok, Result
from sqlalchemy import delete as delete_row
from sqlalchemy import select

from ..database import db
from ..errors import SHORT_ID_ALREADY_EXIST, SHORT_URL_NOT_FOUND
from ..models import ShortUrl


def save(short_url: str, user_id: str, url: str) -> Result[str, str]:
    result = db.session.execute(
        select(ShortUrl).filter_by(short_url=short_url)
    ).scalar()
    # No id collision
    if result is None:
        db.session.add(
            ShortUrl(short_url=short_url, original_url=url, owner_id=user_id)
        )
        db.session.commit()
        return Ok(short_url)

    # Url is already shorten, returns saved short_id
    if result.owner_id == user_id and result.original_url == url:
        return Ok(short_url)

    # Unexpected collision on short_id
    return Err(SHORT_ID_ALREADY_EXIST)


def delete(short_url: str) -> Result[str, str]:
    result = db.session.execute(
        delete_row(ShortUrl).filter_by(short_url=short_url).returning(ShortUrl)
    ).scalar()

    if result is None:
        return Err(SHORT_URL_NOT_FOUND)
    return Ok(result.original_url)


def find(short_url: str) -> Result[ShortUrl, str]:
    result = db.session.execute(
        select(ShortUrl).filter_by(short_url=short_url)
    ).scalar()
    if result is None:
        return Err(SHORT_URL_NOT_FOUND)
    else:
        return Ok(result)
