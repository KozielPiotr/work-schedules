from app import db, login
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


workplaces = db.Table("workplaces",
                     db.Column("worker", db.Integer, db.ForeignKey("user.id")),
                     db.Column("workplace", db.Integer, db.ForeignKey("shop.id")))


class User(UserMixin, db.Model):
    __table_args__ = {"extend_existing": True}
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    access_level = db.Column(db.String(64), index=True, default="2", nullable=False)
    workers_shop = db.relationship("Shop", secondary=workplaces, backref=db.backref("works", lazy="dynamic"))

    def __repr__(self):
        return "{}".format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Shop(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    shopname = db.Column(db.String(64), index=True, unique=True)

    def __repr__(self):
        return "{}".format(self.shopname)

class Billing_period(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    begin = db.Column(db.Integer)
    duration = db.Column(db.Integer)


class Schedule(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True, index=True, nullable=False)
    name = db.Column(db.String, unique=True, index=True)
    year = db.Column(db.Integer)
    month = db.Column(db.Integer)
    workplace = db.Column(db.String)
    ind = db.relationship("Personal_schedule", backref="includes")


class Personal_schedule(db.Model):
    id = db.Column(db.String, primary_key=True, unique=True, index=True, nullable=False)
    date = db.Column(db.DateTime, index=True)
    worker = db.Column(db.String)
    begin_hour = db.Column(db.Integer)
    end_hour = db.Column(db.Integer)
    hours_sum = db.Column(db.Integer)
    event = db.Column(db.String)
    workplace = db.Column(db.String)
    includes_id = db.Column(db.Integer, db.ForeignKey("schedule.id"))


@login.user_loader
def load_user(id):
    return User.query.get(int(id))