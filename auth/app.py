from fastapi import Form, HTTPException, APIRouter
from auth.models import CreatingUser, RetrievingUser
import auth.services as services


auth = APIRouter()


@auth.post('/api/v1/auth/registration/',
           status_code=201,
           response_model=RetrievingUser,
           tags=['users'],
           description='Create new user')
def post_user(creating_user: CreatingUser):
    if created_user := services.create_user(creating_user):
        return created_user
    else:
        raise HTTPException(400)


@auth.get('/api/v1/auth/users/',
          status_code=200,
          response_model=list[RetrievingUser],
          tags=['users'],
          description='Retrieve all users')
def get_users():
    return services.retrieve_users()


@auth.get('/api/v1/auth/users/{user_id}/',
          status_code=200,
          response_model=RetrievingUser,
          tags=['users'],
          description='Create user by ID')
def get_user(user_id: int):
    return services.retrieve_user(user_id)


@auth.post('/api/v1/auth/authorization/', status_code=202, tags=['users'], description='Authorize user')
def post_user(login: str = Form(), password: str = Form()):
    if services.authorize_user(login, password):
        return {'message': 'OK'}
    else:
        raise HTTPException(401)
