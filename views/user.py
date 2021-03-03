from flask import Blueprint
from functools import wraps
from flask import g, request, current_app
from models.user import Account
from errors import *
import jwt

user = Blueprint('user', __name__, url_prefix='/api')


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # check if JWT exists in auth header
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            raise Unauthorised('No authorization header')

        # get jwt
        bearer_token = auth_header.split(sep=' ')[1]

        try:
            payload = jwt.decode(
                bearer_token,
                current_app.config.get('SECRET_KEY'),
                algorithms=['HS256']
            )
        except jwt.exceptions.ExpiredSignatureError:
            raise Unauthorised('Token is expired')

        except jwt.exceptions.InvalidSignatureError:
            raise Unauthorised('Invalid Token')

        except jwt.exceptions.InvalidTokenError:
            raise Unauthorised('Invalid Token')

        # get user
        logged_in_user = Account.objects(id=payload['user_id']).first()
        if user is None:
            raise NotFound('User not found')

        g.user = logged_in_user
        return f(*args, **kwargs)

    return decorated_function


# This route will depend on a middleware that will check the request header for JWTs and pass the user object to this
# route(if possible)
@user.route('/test_route', methods=['GET'])
@login_required
def test_route():
    print(g.user)
    return "Logged in user's name is: " + g.user.profile['name']
