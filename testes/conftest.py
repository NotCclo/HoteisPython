from sql_alchemy import banco
import pytest
from app import app
import sqlalchemy
import json

def session_commit(self):
    banco.session.add(self)
    banco.session.commit()

@pytest.fixture
def client():
    client = app.test_client()
    yield client

def make_headers(jwt):
    return {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': 'Bearer {}'.format(jwt)
            }

def get_access_token(client):
    url = "/login"
    data = {
    "login": "demo",
    "senha": "demo"
    }

    response = client.post(url, data=json.dumps(data), headers={
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            })
    print (response.data)
    object = json.loads(response.data)
    access_token = object["access_token"]
    print (response.status_code)
    return access_token
