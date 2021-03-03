from mongoengine import *
from flask_mongoengine import MongoEngine
import json

db = MongoEngine()


class Profile(EmbeddedDocument):
    name = StringField(required=True)
    username = StringField(required=True)
    email = EmailField(required=True)


class EmailAuth(EmbeddedDocument):
    email = EmailField(required=True)
    password = StringField(required=True)


class Auth(EmbeddedDocument):
    email_auth = EmbeddedDocumentField(EmailAuth)


class Account(db.Document):
    meta = {'collection': 'accounts'}
    auth = EmbeddedDocumentField(Auth)
    profile = EmbeddedDocumentField(Profile)

    def client_json(self):
        return json.loads(self.to_json())['profile']

    @staticmethod
    def new(email: str, hashed_password: str, username: str, name: str):
        return Account(
            auth={
                'email_auth': {
                    'email': email,
                    'password': hashed_password
                }
            },
            profile={
                'name': name,
                'username': username,
                'email': email
            }
        )
