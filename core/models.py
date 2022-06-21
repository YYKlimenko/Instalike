from datetime import datetime
from sqlmodel import Field, SQLModel


class Image(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    user_id: int
    url: str
    text: str | None = None
    date: datetime | None = Field(default_factory=datetime.utcnow)


class CreateImage(SQLModel):
    url: str
    text: str | None = None
    date: datetime | None = Field(default_factory=datetime.utcnow)