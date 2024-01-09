from uuid import uuid4
from sqlalchemy import insert
from sqlalchemy.orm import Session, scoped_session

from bitlypy.models import ApiKey, User

test_uuid = uuid4()
test_user = {"uuid": test_uuid, "email": "test@email.com"}
test_api_key = {"key": "A" * 32, "user_id": test_uuid}


def insert_test_data(session: scoped_session[Session]):
    # Insert test user
    session.execute(
        insert(User).values(user_id=test_user["uuid"], email=test_user["email"])
    )
    # Insert test api key
    session.execute(
        insert(ApiKey).values(key=test_api_key["key"], user_id=test_user["uuid"])
    )
    session.commit()
