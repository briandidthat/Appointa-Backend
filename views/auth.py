from app import db
from models import User
from exceptions import InvalidUsage
from flask import Blueprint, jsonify, request
from flask_login import login_user, login_required, logout_user
from werkzeug.security import check_password_hash

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['POST'])
def login():
    username = request.json['username']
    password = request.json['password']

    user = User.query.filter_by(username=username).first()

    if not user and not check_password_hash(user.password, password):
        raise InvalidUsage('Incorrect login credentials.')

    login_user(user)
    return user.username


@auth.route('/register', methods=['GET', 'POST'])
def register():
    data = map_json_to_user(request.json)
    user = User.query.filter_by(username=data.username).first()

    if user:
        raise InvalidUsage('This user is already registered.', status_code=409)

    db.session.add(data)
    db.session.commit()

    return data.username


@auth.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()


@auth.errorhandler(InvalidUsage)
def invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


def map_json_to_user(data):
    first_name = data['firstName']
    last_name = data['lastName']
    phone_number = data['phoneNumber']
    username = data['username']
    email = data['email']
    password = data['password']
    role = data['role']
    trade = data['trade']

    return User(first_name, last_name, phone_number, username, email, password, role, trade)




