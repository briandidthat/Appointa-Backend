from models import User, Trade, Appointment, Address


def map_json_to_user(data: dict) -> User:
    first_name = data.get('firstName', None)
    last_name = data.get('lastName', None)
    phone_number = data.get('phoneNumber', None)
    username = data.get('username', None)
    email = data.get('email', None)
    password = data.get('password', None)
    type = data.get('type', None)

    return User(first_name, last_name, phone_number, username, email, password, type)


def map_json_to_trade(data: dict) -> Trade:
    code = data.get('code', None)
    name = data.get('name', None)
    description = data.get('description', None)

    return Trade(code, name, description)


def map_json_to_appointment(data: dict) -> Appointment:
    type = data.get('type', None)
    client_id = data.get('clientId', None)
    address_id = data.get('addressId', None)
    description = data.get('description', None)
    date = data.get('date', None)
    time = data.get('time', None)

    return Appointment(type, client_id, address_id, description, date, time)


def map_json_to_address(data: dict) -> Address:
    user_id = data.get('userId', None)
    street = data.get('street', None)
    street2 = data.get('street2', None)
    city = data.get('city', None)
    state = data.get('state', None)
    zip_code = data.get('zipCode')

    return Address(user_id, street, street2, city, state, zip_code)