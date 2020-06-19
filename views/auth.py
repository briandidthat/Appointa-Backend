from app import db, auth_required
from models import User, Role
from utils import map_json_to_user
from exceptions import InvalidUsage
from flask import Blueprint, jsonify, request
from werkzeug.security import check_password_hash
from flask_jwt_extended import create_access_token, get_jwt_identity


auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['POST'])
def login():
    username = request.json.get('username', None)
    password = request.json.get('password', None)

    user = User.query.filter_by(username=username).first()

    if not user and not check_password_hash(user.password, password):
        raise InvalidUsage('Invalid login credentials.', status_code=401)

    access_token = create_access_token(identity=user)

    return jsonify(access_token=access_token), 200


@auth.route('/register', methods=['POST'])
def register():
    data = map_json_to_user(request.json)
    user = User.query.filter_by(username=data.username).first()

    if user:
        raise InvalidUsage('This user is already registered.', status_code=409)

    db.session.add(data)
    role = Role.query.filter_by(name='USER').first()
    data.roles.append(role)
    db.session.commit()

    access_token = create_access_token(data)

    return jsonify(access_token=access_token), 200


@auth.route('/user/me', methods=['GET'])
@auth_required
def get_info():
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200


@auth.errorhandler(InvalidUsage)
def invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response





