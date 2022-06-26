from sqlmodel import SQLModel, Session
from core.db import engine


# Методы взаимодействия с базой данных
def write_to_database(instance: SQLModel):
    with Session(engine) as session:
        session.add(instance)
        session.commit()
        session.refresh(instance)
    return instance


def delete_from_database(model: object, record_id: int):
    with Session(engine) as session:
        instance = session.query(model).filter(model.id == record_id)
        instance.delete()
        session.commit()
