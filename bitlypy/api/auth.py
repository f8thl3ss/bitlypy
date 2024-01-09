import functools

from flask import abort, g, request
from result import Err, Ok

from bitlypy.repositories.auth import get_user_id


def auth_required(view):
    """Validate api key and set `user_id` in global request object."""

    @functools.wraps(view)
    def wrapped_view(**kwargs):
        authorization = request.authorization

        if authorization:
            if authorization.type != "apikey":
                return abort(401, "Unexpected authorization scheme")
            if authorization.token is None:
                return abort(400, "Authorization token is not present")
            maybe_user_id = get_user_id(authorization.token)
            match maybe_user_id:
                case Ok(user_id):
                    g.user_id = user_id
                    return view(**kwargs)
                case Err(_):
                    pass
        return abort(401, "Unauthorized")

    return wrapped_view
