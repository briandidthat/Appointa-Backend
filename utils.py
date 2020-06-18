from models import User, Trade, Appointment


def map_json_to_user(data) -> User:
    first_name = data['firstName']
    last_name = data['lastName']
    phone_number = data['phoneNumber']
    username = data['username']
    email = data['email']
    password = data['password']
    trade = data['trade']

    return User(first_name, last_name, phone_number, username, email, password, role, trade)


def map_json_to_trade(data) -> Trade:
    code = data.get('code', None)
    type = data.get('type', None)
    description = data.get('description', None)

    return Trade(code, type, description)


def map_json_to_appointment(data) -> Appointment:
    provider_id = data.get('provider_id', None)
    client_id = data.get('client_id', None)
    type = data.get('type', None)
    description = data.get('description', None)
    date = data.get('date', None)
    time = data.get('time', None)

    return Appointment(provider_id, client_id, type, description, date, time)
