from uuid import UUID
from result import Result, Ok, Err

from sqlalchemy import select

from ..database import db
from bitlypy.models import ApiKey
from ..errors import API_KEY_NOT_FOUND


def get_user_id(api_key: str) -> Result[UUID, str]:
    result = db.session.execute(select(ApiKey).filter_by(key=api_key)).scalar()
    if result is not None:
        return Ok(result.user_id)
    return Err(API_KEY_NOT_FOUND)
