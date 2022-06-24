import os
from shutil import copyfileobj
from datetime import datetime
from fastapi import UploadFile
from sqlmodel import SQLModel, Session
from core.models import Image
from core.db import engine


# Методы взаимодействия с базой данных
def write_to_database(object_data: SQLModel):
    with Session(engine) as session:
        session.add(object_data)
        session.commit()
        session.refresh(object_data)
    return object_data


# Методы CRUD операций
def get_images(user_id: int):
    with Session(engine) as session:
        images = session.query(Image).filter(Image.user_id == user_id)
        return images.all()


def post_image(user_id: int, url: str, image: Image):
    image = Image(user_id=user_id, url=url, **image.dict())
    return write_to_database(image)


#Методы работы с файлами
def is_validate_image_file():
    return True


def is_upload_file(url: str, user_id: int, temp_file: UploadFile):
    if is_validate_image_file():
        if not os.path.exists(f'media/{user_id}'):
            os.mkdir(f'media/{user_id}')
        with open(f'media/{url}', 'wb') as file:
            copyfileobj(temp_file.file, file)
        return True
    else:
        return False


def get_image_url(user_id: int, file: UploadFile, date: datetime):
    url = f'{user_id}/{date}.jpg'.replace(':', '-')
    if is_upload_file(url, user_id, file):
        return url
