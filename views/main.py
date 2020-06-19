from flask import Blueprint, request, jsonify
from models import Appointment, Trade, User, user_trade
from utils import map_json_to_appointment
from flask_jwt_extended import get_jwt_claims
from app import db, admin_required, auth_required

main = Blueprint('main', __name__)


@main.route('/appointments', methods=['GET'])
@admin_required
def get_all_appointments():
    appointments = Appointment.query.all()
    return jsonify(appointments=[a.serialize for a in appointments]), 200


@main.route('/appointments', methods=['POST'])
@auth_required
def create_appointment():
    appointment = map_json_to_appointment(request.json)
    provider_id = get_jwt_claims().get('userId', None)
    provider = User.query.filter_by(id=provider_id).first()

    db.session.add(appointment)
    appointment.provider.append(provider)
    db.session.commit()

    return jsonify(appointment=appointment.serialize()), 200


@main.route("/appointments/<id>", methods=['GET'])
@auth_required
def get_appointments_by_user(id):
    user = User.query.filter_by(id=id).first()
    appointments = []
    if user.user_type == 'CLIENT':
        appointments = Appointment.query.join(User).filter(Appointment.client_id == User.id).all()
    elif user.user_type == 'PROVIDER':
        appointments = user.provider_appointments.all()

    return jsonify(appointments=[a.serialize() for a in appointments]), 200


@main.route('/appointments/appointment-type', methods=['GET'])
@auth_required
def get_appointments_by_type():
    user_id, type = request.args['id'], request.args['type']
    user = User.query.filter_by(id=user_id).first()
    appointments = []

    if user.user_type == 'CLIENT':
        appointments = Appointment.query.join(User).filter_by(client_id=User.id, type=type).all()
    elif user.user_type == 'PROVIDER':
        appointments = User.provider_appointments.filter_by(type=type).all()

    return jsonify(appointments=[a.serialize() for a in appointments]), 200


@main.route('/trades', methods=['GET'])
@auth_required
def get_all_trades():
    trades = Trade.query.all()
    return jsonify(trades=[t.serialize() for t in trades]), 200


@main.route('/trade/<trade>', methods=['GET'])
@auth_required
def get_providers_by_trade(trade):
    providers = User.query.join(user_trade).join(Trade).filter(
        (user_trade.c.user_id == User.id) & (user_trade.c.trade_id == Trade.id)).filter_by(name=trade).all()

    return jsonify(providers=[p.serialize() for p in providers]), 200
