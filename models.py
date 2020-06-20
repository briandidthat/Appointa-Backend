from werkzeug.security import generate_password_hash
from sqlalchemy import ForeignKey
from app import db


# Define User model
class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    phone_number = db.Column(db.String(100))
    username = db.Column(db.String(100), unique=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    user_type = db.Column(db.String(100))
    addresses = db.relationship('Address', backref='user', lazy='dynamic')
    roles = db.relationship('Role', secondary='user_role', lazy='select', backref=db.backref('owner', lazy=True))
    trades = db.relationship('Trade', secondary='user_trade', lazy='select', backref=db.backref('user', lazy=True))
    provider_appointments = db.relationship('Appointment', secondary='user_appointment', lazy='dynamic',
                                            backref=db.backref('service_provider', lazy=True))

    def __init__(self, first_name, last_name, phone_number, username, email, password, user_type):
        self.first_name = first_name
        self.last_name = last_name
        self.phone_number = phone_number
        self.username = username
        self.email = email
        self.password = generate_password_hash(password, method='sha256')
        self.user_type = user_type

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def serialize(self):
        return {
            "userId": self.id,
            "firstName": self.first_name,
            "lastName": self.last_name,
            "phoneNumber": self.phone_number,
            "username": self.username,
            "email": self.email,
            "userType": self.user_type
        }


# Define address model
class Address(db.Model):
    __tablename__ = 'address'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'))
    street = db.Column(db.String(100))
    street2 = db.Column(db.String(100))
    city = db.Column(db.String(50))
    state = db.Column(db.String(50))
    zip_code = db.Column(db.String(50))

    def __init__(self, user_id, street, street2, city, state, zip_code):
        self.user_id = user_id
        self.street = street
        self.street2 = street2
        self.city = city
        self.state = state
        self.zip_code = zip_code

    def serialize(self):
        return {
            "addressId": self.id,
            "userId": self.user_id,
            "street": self.street,
            "street2": self.street2,
            "city": self.city,
            "state": self.state,
            "zipCode": self.zip_code
        }


# Define appointment model
class Appointment(db.Model):
    __tablename__ = 'appointment'
    id = db.Column(db.Integer, primary_key=True)
    address_id = db.Column(db.Integer, ForeignKey("address.id", ondelete='CASCADE'), nullable=False)
    client_id = db.Column(db.Integer, ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    type = db.Column(db.String(100))
    description = db.Column(db.String(100))
    date = db.Column(db.DateTime, nullable=False)
    time = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(100))
    provider = db.relationship('User', secondary='user_appointment', lazy='select',
                               backref=db.backref('appointment', lazy=True))

    def __init__(self, type, address_id, client_id, description, date, time):
        self.type = type
        self.address_id = address_id
        self.client_id = client_id
        self.description = description
        self.date = date
        self.time = time
        self.status = 'PENDING'

    def __repr__(self):
        return '<Appointment {}>'.format(self.type)

    def serialize(self):
        return {
            "appointmentId": self.id,
            "addressId": self.address_id,
            "clientId": self.client_id,
            "type": self.type,
            "description": self.description,
            "date": self.date,
            "time": self.time,
            "status": self.status
        }


# Define the Role data-model
class Role(db.Model):
    __tablename__ = 'role'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)

    def __init__(self, name):
        self.name = name


# Define trade model
class Trade(db.Model):
    __tablename__ = 'trade'
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(100), unique=True)
    name = db.Column(db.String(100))
    description = db.Column(db.String(100))

    def __init__(self, code, name, description):
        self.code = code
        self.name = name
        self.description = description

    def __repr__(self):
        return '<Trade {}>'.format(self.type)

    def serialize(self):
        return {
            "tradeId": self.id,
            "code": self.code,
            "name": self.name,
            "description": self.description
        }


user_role = db.Table('user_role',
                     db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
                     db.Column('role_id', db.Integer, db.ForeignKey('role.id'), primary_key=True)
                     )

user_trade = db.Table('user_trade',
                      db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
                      db.Column('trade_id', db.Integer, db.ForeignKey('trade.id'), primary_key=True)
                      )

user_appointment = db.Table('user_appointment',
                            db.Column('provider_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
                            db.Column('appointment_id', db.Integer, db.ForeignKey('appointment.id'), primary_key=True)
                            )
