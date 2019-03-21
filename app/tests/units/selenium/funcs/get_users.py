from app import db
from app.models import User


def get_usernames():
    users = []
    for user in User.query.all():
        users.append(user.username)
    return users


def add_user(username, password, access):
    worker = User(username=username, access_level=access)
    worker.set_password(password)
    db.session.add(worker)
    db.session.commit()


def remove_user(username):
    user = User.query.filter_by(username=username).first()
    db.session.delete(user)
    db.session.commit()
