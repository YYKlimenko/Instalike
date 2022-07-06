from datetime import datetime
from sqlmodel import Field, SQLModel, Relationship
from pydantic import EmailStr, validator


class BaseUser(SQLModel):
    username: str = Field(max_length=30, index=True)
    email: EmailStr


class CreatingUser(BaseUser, SQLModel):
    password: str = Field(max_length=256)
    password2: str = Field(max_length=256)

    @validator('password2')
    def match_passwords(cls, password2, values, **kwargs):
        password = values.get('password')
        if password and password2 != password:
            raise ValueError('Passwords don\'t match')
        else:
            return password2


class RetrievingUser(BaseUser):
    id: int = Field(primary_key=True)
    date_registration: datetime = datetime.utcnow()
    is_admin: bool = False


class User(RetrievingUser, table=True):
    hashed_password: str = Field(max_length=256)
    images: list["Image"] | None = Relationship(back_populates="user")