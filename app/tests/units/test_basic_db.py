"""Basic tests"""


from app.models import User
from app.tests.fixtures import client, init_database


def test_add_user(client, init_database):
	assert User.query.filter_by(username="test admin").first().username == "test admin"


def test_set_password(client, init_database):
	u = User(username="test user")
	u.set_password("test_pswd")
	assert u.check_password("test_pswd") is True


def test_connection(client, init_database):
	response = client.get("/login")
	assert response.status_code == 200