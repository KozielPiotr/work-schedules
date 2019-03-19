"""Basic pytests"""

import pytest
from app import app, db
from app.models import User


@pytest.fixture(scope="function")
def client():
	app.config['TESTING'] = True
	app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'
	app.login_manager.init_app(app)
	yield app.test_client()


@pytest.fixture(scope="function")
def init_database():
	db.create_all()
	user1 = User(username="test admin", access_level="0")
	user1.set_password("test_pswd")
	db.session.add(user1)
	db.session.commit()
	yield db
	db.drop_all()


def test_add_user(client, init_database):
	assert User.query.filter_by(username="test admin").first().username == "test admin"


def test_set_password(client, init_database):
	u = User(username="test user")
	u.set_password("test_pswd")
	assert u.check_password("test_pswd") is True


def test_connection(client, init_database):
	response = client.get("/login")
	assert response.status_code == 200
