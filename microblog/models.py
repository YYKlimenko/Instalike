from datetime import datetime
from sqlmodel import Field, SQLModel


class CreateImage(SQLModel):
    text: str | None = Field(max_length=300)


class Image(CreateImage, table=True):
    id: int = Field(default=None, primary_key=True)
    user_id: int
    url: str
    date: datetime | None = Field(default_factory=datetime.utcnow)
