from app import db
from models import User
from flask import Blueprint, request
from flask_login import login_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')

    user = User.query.filter_by(username=username).first()

    if not user and not check_password_hash(user.password, password):
        return 'user not found'

    login_user(user)
    return user.username


@auth.route('/register', methods=['GET', 'POST'])
def register():
    from_post = request.json

    username = from_post['username']
    password = from_post['password']
    email = from_post['email']

    print(username)
    print(password)
    print(email)

    user = User.query.filter_by(username=username).first()

    if user:
        return 'user already register'

    new_user = User(username=username, email=email, password=generate_password_hash(password, method='sha256'))
    db.session.add(new_user)
    db.session.commit()

    return new_user.username
