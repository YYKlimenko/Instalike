import os
from shutil import copyfileobj
from datetime import datetime
from fastapi import UploadFile
from sqlmodel import Session
from core.db import engine
from core.services import write_to_database, delete_from_database
from microblog.models import Image


# Методы CRUD операций
def retrieve_images(user_id: int):
    with Session(engine) as session:
        images = session.query(Image).filter(Image.user_id == user_id)
    return images.all()


def retrieve_image(image_id: int):
    with Session(engine) as session:
        image = session.query(Image).get(image_id)
    return image


def create_image(user_id: int, url: str, image: Image):
    image = Image(user_id=user_id, url=url, **image.dict())
    return write_to_database(image)


def delete_image(image_id):
    image = retrieve_image(image_id)
    delete_from_database(Image, image_id)
    delete_file(image.url)


def update_image(image_id, text):
    with Session(engine) as session:
        image = session.query(Image).filter(Image.id == image_id)
        image.update({'text': text})
        session.commit()
    return image.first()


#Методы работы с файлами
def is_validate_image_file(file: UploadFile):
    if file.content_type == 'image/jpeg':
        return True


def is_upload_file(url: str, user_id: int, temp_file: UploadFile):
    if is_validate_image_file(temp_file):
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


def delete_file(image_url):
    os.remove(f'media/{image_url}')
