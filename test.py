from bcrypt import hashpw, gensalt
from fastapi import UploadFile, Form, Depends
from fastapi.security import HTTPBearer
from fastapi.testclient import TestClient
from sqlmodel import create_engine, Session, SQLModel
from core.db import create_database, get_session, write_to_database
from core.settings import TEST_DATABASE_URL
from main import app
from microblog.app import microblog
import microblog.models
from auth.services import encode_jwt, handle_auth
import auth.models


database_url = f'{TEST_DATABASE_URL}'
engine = create_engine(database_url, echo=False)


def get_test_session():
    with Session(engine) as session:
        yield session


def test_auth():
    return {'sub': 1}


app.dependency_overrides[get_session] = get_test_session
app.dependency_overrides[handle_auth] = test_auth
client = TestClient(app)


def setup():
    SQLModel.metadata.drop_all(engine)
    create_database(engine)
    create_test_data()
    
    
def create_test_data():
    user_1 = auth.models.User(username='user_1',
                              email='user1@test.ru',
                              is_admin='False',
                              hashed_password=hashpw('password1'.encode(), gensalt()))
    user_2 = auth.models.User(username='user_2',
                              email='user2@test.ru',
                              is_admin='False',
                              hashed_password=hashpw('password2'.encode(), gensalt()))
    admin = auth.models.User(username='admin',
                             email='admin@admin.ru',
                             is_admin='True',
                             hashed_password=hashpw('admin'.encode(), gensalt()))
    image_1 = microblog.models.Image(text='Test Image 1. Owner — user_1',
                                     url='/test/1/1.jpg',
                                     user=user_1)
    image_2 = microblog.models.Image(text='Test Image 2. Owner — user_1',
                                     url='/test/1/2.jpg',
                                     user=user_1)
    image_3 = microblog.models.Image(text='Test Image 3. Owner — user_2',
                                     url='/test/1/3.jpg',
                                     user=user_2)
    with Session(engine) as session:
        write_to_database([user_1, user_2, admin, image_1, image_2, image_3], session)
    with open('media/test/1/1.jpg', 'w'):
        pass


def test_get_images():
    response = client.get('/api/v1/1/')
    assert response.status_code == 200
    response_json = response.json()
    for instance in response_json:
        instance.pop('date')
    assert response_json == [
                                {'url': '/test/1/1.jpg',
                                 'id': 1,
                                 'user_id': 1,
                                 'text': 'Test Image 1. Owner — user_1'},
                                {'url': '/test/1/2.jpg',
                                 'id': 2,
                                 'user_id': 1,
                                 'text': 'Test Image 2. Owner — user_1'}
                              ]


def test_get_image():
    response = client.get('/api/v1/images/1/')
    assert response.status_code == 200
    response_json = response.json()
    response_json.pop('date')
    assert response_json == {'url': '/test/1/1.jpg',
                             'id': 1,
                             'user_id': 1,
                             'text': 'Test Image 1. Owner — user_1'}


def test_post_image():
    with open('media/test/test.jpg', 'rb') as f:
        file_data = f.read()
    response = client.post('/api/v1/1/', data={'text': 'Hello World'},
                           files={'file': ('test.jpg', file_data, 'image/jpeg')})
    assert response.status_code == 201
    response_json = response.json()
    response_json.pop('url')
    response_json.pop('date')
    assert response_json == {'id': 4,
                             'user_id': 1,
                             'text': 'Hello World'}


def test_update_image():
    response = client.put('/api/v1/images/1/', {'image_id': 1, 'text': 'Updated text'})
    print(response.json())
    assert response.status_code == 201
    response = client.get('/api/v1/images/1/')
    response_json = response.json()
    response_json.pop('date')
    assert response_json == {'url': '/test/1/1.jpg',
                             'id': 1,
                             'user_id': 1,
                             'text': 'Updated text'}


def test_delete_image():
    response = client.delete('/api/v1/images/4/', json={'id': 4})
    assert response.status_code == 204
    response = client.get('/api/v1/images/4/')
    assert not response.json()


def test_get_users():
    response = client.get('/api/v1/auth/users/')
    assert response.status_code == 200
    response_json = response.json()
    for instance in response_json:
        instance.pop('date_registration')
    assert response_json == [
                                {'username': 'user_1',
                                 'email': 'user1@test.ru',
                                 'id': 1,
                                 'is_admin': False},
                                {'username': 'user_2',
                                 'email': 'user2@test.ru',
                                 'id': 2,
                                 'is_admin': False},
                                {'username': 'admin',
                                 'email': 'admin@admin.ru',
                                 'id': 3,
                                 'is_admin': True},
                              ]


def test_get_user():
    response = client.get('/api/v1/auth/users/1/')
    assert response.status_code == 200
    response_json = response.json()
    response_json.pop('date_registration')
    assert response_json == {'username': 'user_1',
                             'email': 'user1@test.ru',
                             'id': 1,
                             'is_admin': False}


def test_authorization():
    response = client.post('/api/v1/auth/authorization/', {'username': 'user_1', 'password': 'password1'})
    assert response.status_code == 202
    assert response.json() == {"access_token": encode_jwt(1), "token_type": "bearer"}

