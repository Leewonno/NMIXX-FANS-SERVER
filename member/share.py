from graphql_jwt.exceptions import JSONWebTokenError
from graphql_jwt.shortcuts import get_user_by_token


def get_member_from_token(token, context):
    """
    토큰을 이용해 Django User와 연결된 Member를 반환
    """
    try:
        user = get_user_by_token(token, context)
        if user is None:
            return None
        member = getattr(user, "member", None)
        return member
    except JSONWebTokenError:
        return None
