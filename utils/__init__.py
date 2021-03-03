import jwt
import datetime


def generate_access_and_refresh_tokens(access_token_key: str, refresh_token_key: str, user_id: str) -> dict:
    access_token = jwt.encode(
        {
            'exp': datetime.datetime.now().timestamp() + (5 * 60),
            'iss': 'flask_user_auth',
            'iat': datetime.datetime.now().timestamp(),
            'user_id': user_id,
        },
        key=access_token_key,
        algorithm="HS256"
    )

    refresh_token = jwt.encode(
        {
            'exp': datetime.datetime.now().timestamp() + (7 * 24 * 60 * 60),
            'iss': 'flask_user_auth',
            'iat': datetime.datetime.now().timestamp(),
            'user_id': user_id,
        },
        key=access_token_key,
        algorithm="HS256"
    )
    return {
        'access_token': access_token,
        'refresh_token': refresh_token
    }
