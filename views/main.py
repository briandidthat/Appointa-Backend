from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from models import Appointment, Trade, User
from utils import map_json_to_appointment
from app import db

main = Blueprint('main', __name__)


@jwt_required
@main.route('/appointments/<id>', methods=['POST'])
def create_appointment(id):
    provider = User.query.filter_by(id=id).first()
    appointment = map_json_to_appointment(request.json)

    provider.appointments.append(appointment)
    db.session.commit()

    return jsonify(appointment), 200


@jwt_required
@main.route("/appointments/<id>", methods=['GET'])
def get_appointments_by_user(id):
    user = User.query.filter_by(id=id).first()
    appointments = []
    if user.user_type == 'CLIENT':
        appointments = Appointment.query.join(User).filter_by(client_id=User.id).all()
    elif user.user_type == 'PROVIDER':
        appointments = Appointment.query.join(User).filter_by(provider_id=User.id, status='OPEN').all()

    return jsonify(appointments), 200


@jwt_required
@main.route('/appointments/appointment-type', methods=['GET'])
def get_appointments_by_type():
    user_id, type = request.args['id'], request.args['type']
    user = User.query.filter_by(id=user_id).first()
    appointments = []

    if user.user_type == 'CLIENT':
        appointments = Appointment.query.join(User).filter_by(client_id=User.id, type=type).all()
    elif user.user_type == 'PROVIDER':
        appointments = Appointment.query.join(User).filter_by(provider_id=User.id, type=type).all()

    return jsonify(appointments), 200


@jwt_required
@main.route('/trades', methods=['GET'])
def get_all_trades():
    trades = Trade.query.all()
    return jsonify(trades), 200


@jwt_required
@main.route('/trade', methods=['GET'])
def get_providers_by_trade():
    trade_code = request.args['trade_code']
    user_list = User.query.filter_by(trade_code=trade_code, user_type='PROVIDER').all()
    return jsonify(user_list), 200
