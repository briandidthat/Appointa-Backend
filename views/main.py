from typing import Tuple, Sequence

from flask import Blueprint, request, jsonify
from models import Appointment, Trade, User, user_trade, Address
from utils import map_json_to_appointment, map_json_to_address
from flask_jwt_extended import get_jwt_claims
from app import db, auth_required, admin_required

main = Blueprint('main', __name__)


@main.route('/appointments', methods=['GET'])
@admin_required
def get_all_appointments() -> Tuple[Sequence[Appointment], int]:
    appointments = Appointment.query.all()
    return jsonify(appointments=[a.serialize() for a in appointments]), 200


@main.route('/appointments', methods=['POST'])
@auth_required
def create_appointment() -> Tuple[Appointment, int]:
    appointment = map_json_to_appointment(request.json)
    provider_id = get_jwt_claims().get('userId', None)
    provider = User.query.filter_by(id=provider_id).first()

    db.session.add(appointment)
    appointment.provider.append(provider)
    provider.service_provider.append(appointment)
    db.session.commit()

    return jsonify(appointment=appointment.serialize()), 200


@main.route('/addresses', methods=['POST'])
@auth_required
def create_address() -> Tuple[Address, int]:
    address = map_json_to_address(request.json)
    user = User.query.filter_by(id=address.user_id).first()

    db.session.add(address)
    user.addresses.append(address)
    db.session.commit()

    return jsonify(address=address.serialize()), 200


@main.route("/addresses/<id>", methods=['GET'])
@auth_required
def get_addresses_by_user(id) -> Tuple[Sequence[Address], int]:
    user = User.query.filter_by(id=id).first()
    return jsonify(addresses=[a.serialize() for a in user.addresses]), 200


@main.route("/appointments/<id>", methods=['GET'])
@auth_required
def get_appointments_by_user(id) -> Tuple[Sequence[Appointment], int]:
    user = User.query.filter_by(id=id).first()
    appointments = []
    if user.user_type == 'CLIENT':
        appointments = Appointment.query.join(User).filter(Appointment.client_id == User.id).all()
    elif user.user_type == 'PROVIDER':
        appointments = user.provider_appointments.all()

    return jsonify(appointments=[a.serialize() for a in appointments]), 200


@main.route('/appointments/appointment-type', methods=['GET'])
@auth_required
def get_appointments_by_type() -> Tuple[Sequence[Appointment], int]:
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
def get_all_trades() -> Tuple[Sequence[Trade], int]:
    trades = Trade.query.all()
    return jsonify(trades=[t.serialize() for t in trades]), 200


@main.route('/providers/trades/<trade>', methods=['GET'])
@auth_required
def get_providers_by_trade(trade) -> Tuple[Sequence[User], int]:
    providers = User.query.join(user_trade).join(Trade).filter(
        (user_trade.c.user_id == User.id) & (user_trade.c.trade_id == Trade.id)).filter_by(name=trade).all()

    return jsonify(providers=[p.serialize() for p in providers]), 200
