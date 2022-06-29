from sqlmodel import SQLModel, Session, create_engine, exists
import microblog.models
import auth.models


database_url = f'sqlite:///core/database.db'
engine = create_engine(database_url, echo=True)


def create_database(applications: tuple = (microblog.models, auth.models)):
    for application in applications:
        application.SQLModel.metadata.create_all(engine)


def write_to_database(instance: SQLModel):
    with Session(engine) as session:
        session.add(instance)
        session.commit()
        session.refresh(instance)
    return instance


def retrieve_from_database(model: object, instance_id: int | str, key: str = 'id', many: bool = False):
    with Session(engine) as session:
        if key == 'username':
            instances = session.query(auth.models.User)
            if not many:
                instances = session.query(auth.models.User).filter(auth.models.User.username == instance_id).first()
        else:
            instances = session.query(model).get(instance_id)
    return instances


def retrieve_from_database_by_user(model, user_id: int):
    with Session(engine) as session:
        instance = session.query(model).filter(model.user_id == user_id)
    return instance.all()


def delete_from_database(model, instance_id: int):
    with Session(engine) as session:
        instance = session.query(model).filter(model.id == instance_id)
        instance.delete()
        session.commit()


def update_in_database(model: object, instance_id: int, data: dict):
    with Session(engine) as session:
        instance = session.query(model).filter(model.id == instance_id)
        instance.update(data)
        session.commit()
    return instance.first()


def check_user_exists(username: str) -> bool:
    with Session(engine) as session:
        user_exists = session.query(exists().where(auth.models.User.username == username)).scalar()
    if user_exists:
        return True
    else:
        return False


if __name__ == '__main__':
    create_database()
