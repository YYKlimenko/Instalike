from sqlmodel import SQLModel, Session, create_engine, exists
from bcrypt import hashpw, gensalt
from core.settings import DATABASE_URL
import microblog.models
import auth.models

database_url = f'{DATABASE_URL}'
engine = create_engine(database_url, echo=False)


def get_session():
    with Session(engine) as session:
        yield session


def create_database(engine, applications: tuple = (microblog.models, auth.models)):
    for application in applications:
        application.SQLModel.metadata.create_all(engine)


def write_to_database(instances: list[SQLModel] | SQLModel, session: Session):
    if isinstance(instances, SQLModel):
        instances = (instances,)
    for instance in instances:
        session.add(instance)
    session.commit()


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
    create_database(engine=engine)
    admin = auth.models.User(username='admin',
                             email='admin@admin.ru',
                             is_admin='True',
                             hashed_password=hashpw('admin'.encode(), gensalt()))
    write_to_database(admin, Session(engine))
