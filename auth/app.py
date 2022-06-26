from fastapi import Form, HTTPException, APIRouter
from auth.models import CreatingUser, RetrievingUser
import auth.services as services


auth = APIRouter()


@auth.post('/api/v1/auth/registration/', status_code=201, response_model=RetrievingUser)
def post_user(user: CreatingUser):
    created_user = services.create_user(user)
    if created_user:
        return created_user
    else:
        raise HTTPException(400)


@auth.get('/api/v1/auth/users/', status_code=200, response_model=list[RetrievingUser])
def get_users():
    return services.retrieve_users()


@auth.get('/api/v1/auth/users/{username}/', status_code=200, response_model=RetrievingUser)
def get_user(username: str):
    return services.retrieve_user(username)


@auth.post('/api/v1/auth/authorization/', status_code=202)
def post_user(login: str = Form(), password: str = Form()):
    if services.authorize_user(login, password):
        return {'message': 'OK'}
    else:
        raise HTTPException(401)
