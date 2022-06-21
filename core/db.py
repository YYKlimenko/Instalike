from sqlmodel import create_engine
import core.models

database_url = f'sqlite:///core/database.db'
engine = create_engine(database_url, echo=True)


def migrate():
    core.models.SQLModel.metadata.create_all(engine)


if __name__ == '__main__':
    migrate()
