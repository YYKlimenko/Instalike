from datetime import datetime
from sqlmodel import Field, SQLModel, Relationship
from auth.models import User


class CreateImage(SQLModel):
    text: str | None = Field(max_length=300)


class Image(CreateImage, table=True):
    id: int = Field(primary_key=True)
    url: str
    date: datetime | None = Field(default_factory=datetime.utcnow)
    user_id: int = Field(foreign_key="user.id")
    user: User = Relationship(back_populates='images')
