from sqlmodel import create_engine
from core.settings import DATABASE_URL
import core.models


engine = create_engine(DATABASE_URL, echo=True)


def migrate():
    core.models.SQLModel.metadata.create_all(engine)


if __name__ == '__main__':
    migrate()
