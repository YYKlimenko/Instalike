from datetime import datetime
from sqlmodel import Field, SQLModel
from pydantic import EmailStr, validator


class CreateUser(SQLModel):
    username: str = Field(max_length=30, index=True)
    password: Field(max_length=256)
    password2: Field(max_length=256)
    email: EmailStr = Field(max_length=120)

    @validator('password2')
    def match_passwords(cls, password2, values):
        password = values.get('password')
        if password and password2 != password:
            raise ValueError('Passwords don\'t match')


class User(CreateUser, table=True):
    id: int = Field(primary_key=True)
    hashed_password: str = Field(max_length=256)
    is_admin: bool = False
    date_registration: datetime = datetime.utcnow()
