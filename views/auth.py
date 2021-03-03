from flask import current_app, Blueprint, request
from validation import RegisterRequestSchema, LoginRequestSchema
from errors import *
from models.user import Account
import bcrypt
from marshmallow import ValidationError
from utils import generate_access_and_refresh_tokens

auth = Blueprint('auth', __name__, url_prefix='/api/auth')


@auth.errorhandler(ValidationError)
def error_handler(error):
    # return first error
    print(error.messages)
    for key in error.messages:
        print(key)
        return {
                   'message': error.messages[key][0]
               }, BadRequest.status_code


@auth.route('/login', methods=['POST'])
def login():
    if request.get_json():
        req = LoginRequestSchema().load(request.get_json())
        if 'username' in req:
            user = Account.objects(profile__username=req['username']).first()
        else:
            user = Account.objects(auth__email_auth__email=req['email']).first()

        if user is None:
            raise NotFound("User does not exist!")

        is_correct_password = bcrypt.checkpw(req['password'].encode(), user.auth.email_auth['password'].encode())

        if is_correct_password:
            tokens = generate_access_and_refresh_tokens(
                access_token_key=current_app.config.get("SECRET_KEY"),
                refresh_token_key=current_app.config.get("SECRET_KEY"),
                user_id=str(user.id)
            )
            return {
                'data': user.client_json(),
                'token_details': {
                    'access_token': tokens["access_token"],
                    'refresh_token': tokens["refresh_token"]
                }
            }
        else:
            raise Unauthorised("Incorrect password!")
    else:
        return BadRequest('Send request body as JSON')


@auth.route('/register', methods=['POST'])
def register():
    if request.get_json():
        req = RegisterRequestSchema().load(request.get_json())

        hashed_password = bcrypt.hashpw(req['password'].encode(), bcrypt.gensalt())
        if Account.objects(auth__email_auth__email=req['email']):
            raise AppException(409, 'User already exists')

        user = Account.new(
            email=req['email'],
            hashed_password=hashed_password.decode(),
            username=req['username'],
            name=req['name']
        )

        # save user to db
        user.save()

        # generate access and refresh tokens
        tokens = generate_access_and_refresh_tokens(
            access_token_key=current_app.config.get('SECRET_KEY'),
            refresh_token_key=current_app.config.get('SECRET_KEY'),
            user_id=str(user.id)
        )

        return {
           'data': user.client_json(),
           'token_details': {
               'access_token': tokens["access_token"],
               'refresh_token': tokens["refresh_token"]
           }
        }, 201
    else:
        raise BadRequest('Send request body as json')
