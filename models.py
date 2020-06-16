from flask_login import UserMixin
from werkzeug.security import generate_password_hash
from app import db


class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    phone_number = db.Column(db.String(100))
    username = db.Column(db.String(100), unique=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    role = db.Column(db.String(100))
    trade = db.Column(db.String(100))
    addresses = db.relationship('Address', backref='owner')
    appointments = db.relationship('Appointment', backref='user')

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


class Address(db.Model):
    __tablename__ = "address"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
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


class Trade(db.Model):
    __tablename__ = 'trade'
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(100), unique=True)
    type = db.Column(db.String(100))
    description = db.Column(db.String(100))

    def __init__(self, code, type, description):
        self.code = code
        self.type = type
        self.description = description

    def __repr__(self):
        return '<Trade {}>'.format(self.type)


class Appointment(db.Model):
    __tablename__ = 'appointment'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    client_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    type = db.Column(db.String(100))
    description = db.Column(db.String(100))
    date = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(100))

    def __init__(self, user_id, type, description, date, status):
        self.user_id = user_id
        self.type = type
        self.description = description
        self.date = date
        self.status = status

    def __repr__(self):
        return '<Appointment {}>'.format(self.type)