from flask import Flask, jsonify
from functools import wraps
from flask_jwt_extended import JWTManager, get_jwt_claims, verify_jwt_in_request
from flask_sqlalchemy import SQLAlchemy

# instantiate database
db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config.from_object('config.DevelopmentConfig')

    db.init_app(app)

    jwt = JWTManager(app)

    @jwt.user_claims_loader
    def add_claims_to_access_token(user):
        return {
            "userId": user.id,
            "roles": [role.name for role in user.roles]
        }

    @jwt.user_identity_loader
    def user_identity_lookup(user):
        return user.username

    from views import auth, main
    app.register_blueprint(auth)
    app.register_blueprint(main)

    return app


# Custom Decorator to verify that requesting user has admin access
def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        claims = get_jwt_claims()
        if 'ADMIN' not in claims['roles']:
            return jsonify(message="Unauthorized Access."), 403
        else:
            return fn(*args, **kwargs)
    return wrapper


# Custom Decorator to ensure that user is logged in and has passed jwt
def auth_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        claims = get_jwt_claims()
        if 'USER' not in claims['roles']:
            return jsonify(message="Unauthorized Access."), 403
        else:
            return fn(*args, **kwargs)
    return wrapper


if __name__ == '__main__':
    app = create_app()
    app.run()

