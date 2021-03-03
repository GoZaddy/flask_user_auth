from flask import Flask
import os
from errors import *


def create_app():
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object(os.getenv('APP_SETTINGS'))

    @app.route('/api')
    def hello():
        return 'Hello!'

    @app.errorhandler(AppException)
    def handle_bad_request(error):
        return {
            'message': error.message
        }, error.status_code

    @app.errorhandler(500)
    def handle_500():
        return {
            'message': 'Internal Server Error!'
        }, 500

    import views.auth as auth
    import views.user as user

    app.register_blueprint(user.user)
    app.register_blueprint(auth.auth)

    from models.user import db
    db.init_app(app)
    return app



