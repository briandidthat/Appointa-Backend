from flask_login import UserMixin
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
    user_type = db.Column(db.String(100))
    trades = db.relationship('Trade', backref="owner")
    prior_appts = db.relationship('PriorAppts', backref="appt-owner")

    def __repr__(self):
        return '<User {}>'.format(self.username)


class Trade(db.Model):
    __tablename__ = 'trade'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    type = db.Column(db.String(100))
    description = db.Column(db.String(100))

    def __repr__(self):
        return '<Trade {}>'.format(self.type)


class PriorAppts(db.Model):
    __tablename__ = 'prior_appts'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    type = db.Column(db.String(100))
    description = db.Column(db.String(100))
    date = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(100))

    def __repr__(self):
        return '<Prior_Appts {}>'.format(self.type)