from marshmallow import fields, Schema, ValidationError, validates_schema, EXCLUDE, validate


class LoginRequestSchema(Schema):
    email = fields.Str()
    password = fields.Str(required=True)
    username = fields.Str()

    class Meta:
        unknown = EXCLUDE

    @validates_schema
    def validate_userid(self, data, **kwargs):
        errors = {}
        if 'username' in data and 'email' in data:
            errors['user_id'] = ['use email or username not both']

        if 'username' not in data and 'email' not in data:
            errors['user_id'] = ['email or username is required']

        if 'username' in data:
            if len(data['username']) < 1:
                errors['username'] = ['username should have at least one character']

        if 'email' in data:
            if len(data['email']) < 1:
                errors['email'] = ['email field is not a valid email']
            try:
                validate.Email()(data['email'])
            except ValidationError:
                errors['email'] = ['email field is not a valid email']
        if errors:
            raise ValidationError(errors)


class RegisterRequestSchema(Schema):
    name = fields.Str(
        required=True,
        error_messages={'required': 'a name is required'}
    )
    email = fields.Email(
        required=True,
        error_messages={'required': 'an email is required'}
    )
    username = fields.Str(
        required=True,
        error_messages={'required': 'a username is required'}
    )
    password = fields.Str(
        required=True,
        error_messages={'required': 'a password is required'}
    )
