from datetime import datetime
from sqlmodel import Session, exists
from bcrypt import checkpw, gensalt, hashpw
from core.db import engine, write_to_database
from auth.models import User


def check_user_exists(username):
    with Session(engine) as session:
        user_exists = session.query(exists().where(User.username == username)).scalar()
    return user_exists


# Методы CRUD операций
def create_user(creating_user):
    if check_user_exists(creating_user.username):
        return False
    else:
        user = User(username=creating_user.username,
                    email=creating_user.email,
                    hashed_password=get_hashed_password(creating_user.password),
                    is_admin=False,
                    date_registration=datetime.utcnow())
        return write_to_database(user)


def get_hashed_password(password):
    return hashpw(password.encode(), gensalt())


def retrieve_users():
    with Session(engine) as session:
        users = session.query(User)
    return users.all()


def retrieve_user(username: str):
    with Session(engine) as session:
        user = session.query(User).filter(User.username == username).first()
    return user


def authorize_user(login, password):
    user = retrieve_user(login)
    if checkpw(password.encode(), user.hashed_password.encode()):
        return True
