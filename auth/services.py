from datetime import datetime, timedelta

from fastapi import Security, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from bcrypt import checkpw, gensalt, hashpw
import jwt
from core.db import (write_to_database, retrieve_list_from_database,
                     retrieve_instance_from_database, check_user_exists, retrieve_instance_by_username)
from core.settings import SECRET_KEY
from auth.models import User, CreatingUser


# Методы CRUD операций
def create_user(creating_user: CreatingUser):
    if not check_user_exists(creating_user.username):
        user = User(username=creating_user.username,
                    email=creating_user.email,
                    hashed_password=get_hashed_password(creating_user.password),
                    is_admin=False,
                    date_registration=datetime.utcnow())
        return write_to_database(user)


def retrieve_users():
    users = retrieve_list_from_database(User)
    return users.all()


def retrieve_user(user_id: int):
    user = retrieve_instance_from_database(User, user_id)
    return user


# Методы авторизации, аутентификации
def authorize_user(login, password):
    if user_exists := check_user_exists(login):
        user = retrieve_instance_by_username(User, login)
        print(user)
        if checkpw(password.encode(), user.hashed_password.encode()):
            return True
    else:
        return False


def get_hashed_password(password):
    return hashpw(password.encode(), gensalt())


def encode_jwt(user_id):
    payload = {
        'exp': datetime.utcnow() + timedelta(hours=12),
        'iat': datetime.utcnow(),
        'sub': user_id
    }
    return jwt.encode(payload, SECRET_KEY, algorithm='HS256')


def decode_jwt(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail='Expired')
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail='Invalid token')


def handle_auth(auth: HTTPAuthorizationCredentials = Security(HTTPBearer)):
    return decode_jwt(auth.credentials)
