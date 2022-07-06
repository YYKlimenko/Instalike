from fastapi import HTTPException
from core.db import retrieve_instance_from_database
from auth.models import User


def permit_for_owner(func):
    def wrapper(*args, **kwargs):
        if kwargs['user_id'] == kwargs['current_user_id']:
            return func(*args, **kwargs)
        else:
            return HTTPException(401, detail='Not permitted')
    return wrapper
