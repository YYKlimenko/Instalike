from sqlmodel import SQLModel, Session, create_engine, exists
from core.settings import DATABASE_FILE
import microblog.models
import auth.models

database_url = f'sqlite:///{DATABASE_FILE}'
engine = create_engine(database_url, echo=False)


def create_database(applications: tuple = (microblog.models, auth.models)):
    for application in applications:
        application.SQLModel.metadata.create_all(engine)


def write_to_database(instance: SQLModel, session: Session):
    session.add(instance)
    session.commit()
    session.refresh(instance)


def retrieve_list_from_database(model: object, session: Session):
    instances = session.query(model)
    return instances


def retrieve_instance_from_database(model: object, instance_id: int, session: Session):
    instance = session.query(model).get(instance_id)
    return instance


def retrieve_instance_by_username(model: object, username: str, session: Session):
    instances = retrieve_list_from_database(model, session)
    instance = instances.filter(model.username == username).first()
    return instance


def delete_from_database(model, instance_id: int, session: Session):
    instance = session.query(model).filter(model.id == instance_id)
    instance.delete()
    session.commit()


def update_in_database(model: object, instance_id: int, session: Session, data: dict):
    instance = session.query(model).filter(model.id == instance_id)
    instance.update(data)
    session.commit()
    return instance.first()


def check_user_exists(session: Session, username: str | None = None, user_id: int | None = None) -> bool:
    if user_id:
        user_exists = session.query(exists().where(auth.models.User.id == user_id)).scalar()
    if username:
        user_exists = session.query(exists().where(auth.models.User.username == username)).scalar()
    return user_exists


if __name__ == '__main__':
    create_database()
