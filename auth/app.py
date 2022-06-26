from fastapi import FastAPI, Form, HTTPException
from auth.models import CreatingUser, RetrievingUser
import auth.services as services

app = FastAPI()


@app.post('/api/v1/registration/', status_code=201)
def post_user(user: CreatingUser):
    return services.create_user(user)


@app.get('/api/v1/users/', status_code=200, response_model=list[RetrievingUser])
def get_users():
    return services.retrieve_users()


@app.get('/api/v1/users/{username}/', status_code=200, response_model=RetrievingUser)
def get_user(username: str):
    return services.retrieve_user(username)


@app.post('/api/v1/authorization/', status_code=202)
def post_user(login: str = Form(), password: str = Form()):
    if services.authorize_user(login, password):
        return {'message': 'OK'}
    else:
        raise HTTPException(401)
