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
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    access_level = db.Column(db.String(64), index=True, default="u", nullable=False)
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


@login.user_loader
def load_user(id):
    return User.query.get(int(id))