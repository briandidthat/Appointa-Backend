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
    trade_code = db.Column(db.String(100), ForeignKey('trade.code'))
    roles = db.relationship('Role', secondary='user_role')
    addresses = db.relationship('Address', backref='user', lazy='dynamic', foreign_keys='address.user_id')
    provider_appointments = db.relationship('Appointment', backref='provider', lazy='dynamic',
                                            foreign_keys='appointment.provider_id')
    client_appointments = db.relationship('Appointment', backref='client', lazy='dynamic',
                                          foreign_keys='appointment.client_id')

    def __init__(self, first_name, last_name, phone_number, username, email, password, role, trade):
        self.first_name = first_name
        self.last_name = last_name
        self.phone_number = phone_number
        self.username = username
        self.email = email
        self.password = generate_password_hash(password, method='sha256')
        self.role = role
        self.trade = trade

    def __repr__(self):
        return '<User {}>'.format(self.username)


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


# Define trade model
class Trade(db.Model):
    __tablename__ = 'trade'
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(100), unique=True)
    name = db.Column(db.String(100))
    description = db.Column(db.String(100))
    users = db.relationship('User', backref='user')

    def __init__(self, code, name, description):
        self.code = code
        self.name = name
        self.description = description

    def __repr__(self):
        return '<Trade {}>'.format(self.type)


# Define appointment model
class Appointment(db.Model):
    __tablename__ = 'appointment'
    id = db.Column(db.Integer, primary_key=True)
    provider_id = db.Column(db.Integer, ForeignKey("user.id", ondelete='CASCADE'))
    client_id = db.Column(db.Integer, ForeignKey("user.id", ondelete='CASCADE'))
    type = db.Column(db.String(100))
    description = db.Column(db.String(100))
    date = db.Column(db.DateTime, nullable=False)
    time = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(100))

    def __init__(self, provider_id, client_id, type, description, date, time):
        self.provider_id = provider_id
        self.client_id = client_id
        self.type = type
        self.description = description
        self.date = date
        self.time = time
        self.status = 'PENDING'

    def __repr__(self):
        return '<Appointment {}>'.format(self.type)


# Define the Role data-model
class Role(db.Model):
    __tablename__ = 'role'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), unique=True)

    def __init__(self, name):
        self.name = name


# Define the UserRoles association table
class UserRole(db.Model):
    __tablename__ = 'user_role'
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), ForeignKey('user.id', ondelete='CASCADE'))
    role_id = db.Column(db.Integer(), ForeignKey('role.id', ondelete='CASCADE'))

    def __init__(self, user_id, role_id):
        self.user_id = user_id
        self.role_id = role_id
