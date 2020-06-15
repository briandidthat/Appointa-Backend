from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

# instantiate database
db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')

    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)


    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)

