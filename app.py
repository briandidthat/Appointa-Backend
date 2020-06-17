from flask import Flask
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy

# instantiate database
db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')

    db.init_app(app)

    jwt = JWTManager(app)

    from views import auth
    app.register_blueprint(auth)

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)

