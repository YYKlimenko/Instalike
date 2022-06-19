from sqlmodel import Field, SQLModel, create_engine


class Post(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    text: str
    author: str


sqlite_file_name = "db.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(sqlite_url, echo=True)
SQLModel.metadata.create_all(engine)
