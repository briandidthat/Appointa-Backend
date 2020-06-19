from flask import Blueprint, request, jsonify
from models import Appointment, Trade, User, user_trade, user_appointment
from utils import map_json_to_appointment
from app import db, admin_required, auth_required

main = Blueprint('main', __name__)


@main.route('/appointments', methods=['GET'])
@admin_required
def get_all_appointments():
    appointments = Appointment.query.all()
    return jsonify(appointments), 200


@main.route('/appointments', methods=['POST'])
@auth_required
def create_appointment():
    appointment = map_json_to_appointment(request.json)
    provider = User.query.filter_by(id=appointment.provider_id).first()
    client = User.query.filter_by(id=appointment.client_id).first()

    provider.provider_appointments.append(appointment)
    client.client_appointments.append(appointment)
    db.session.add(appointment)
    db.session.commit()

    return jsonify(appointment), 200


@main.route("/appointments/<id>", methods=['GET'])
@auth_required
def get_appointments_by_user(id):
    user = User.query.filter_by(id=id).first()
    appointments = []
    if user.user_type == 'CLIENT':
        appointments = Appointment.query.join(User).filter_by(client_id=User.id).all()
    elif user.user_type == 'PROVIDER':
        appointments = Appointment.query.join(User).filter_by(provider_id=User.id, status='OPEN').all()

    return jsonify(appointments), 200


@main.route('/appointments/appointment-type', methods=['GET'])
@auth_required
def get_appointments_by_type():
    user_id, type = request.args['id'], request.args['type']
    user = User.query.filter_by(id=user_id).first()
    appointments = []

    if user.user_type == 'CLIENT':
        appointments = Appointment.query.join(User).filter_by(client_id=User.id, type=type).all()
    elif user.user_type == 'PROVIDER':
        appointments = Appointment.query.join(User).filter_by(provider_id=User.id, type=type).all()

    return jsonify(appointments), 200


@main.route('/trades', methods=['GET'])
@auth_required
def get_all_trades():
    trades = Trade.query.all()
    return jsonify(trades), 200


@main.route('/trade', methods=['GET'])
@auth_required
def get_providers_by_trade():
    trade_name = request.args.get('trade', None)
    return jsonify(trade_name), 200
