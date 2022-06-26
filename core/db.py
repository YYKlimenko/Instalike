from sqlmodel import create_engine
import microblog.models
import auth.models

database_url = f'sqlite:///core/database.db'
engine = create_engine(database_url, echo=True)


def create():
    microblog.models.SQLModel.metadata.create_all(engine)
    auth.models.SQLModel.metadata.create_all(engine)


if __name__ == '__main__':
    create()
