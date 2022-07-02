import os
from shutil import copyfileobj
from datetime import datetime

from fastapi import UploadFile
from sqlmodel import Session

from core.db import (write_to_database, delete_from_database, retrieve_instance_from_database, update_in_database,
                     engine)
from microblog.models import Image, CreateImage
from auth.models import User


# Методы CRUD операций
def retrieve_images(user_id: int):
    with Session(engine) as session:
        user = retrieve_instance_from_database(User, user_id, session)
        images = user.images
    return images


def retrieve_image(image_id: int):
    with Session(engine) as session:
        image = retrieve_instance_from_database(Image, image_id, session)
    return image


def create_image(user_id: int, temp_file: UploadFile, image: CreateImage):
    url = create_image_url(user_id)
    if upload_file(temp_file, user_id, url):
        with Session(engine) as session:
            image = Image(url=url,
                          user=retrieve_instance_from_database(User, user_id, session),
                          **image.dict())
            write_to_database(image, session)
        return image


def delete_image(image_id):
    with Session(engine) as session:
        if image := retrieve_instance_from_database(Image, image_id, session):
            delete_from_database(Image, image_id, session)
    delete_file(image.url)


def update_image(image_id, text):
    with Session(engine) as session:
        return update_in_database(Image, image_id, session, data={'text': text})


# Методы работы с файлами
def is_validate_image_file(file):
    if file.content_type == 'image/jpeg':
        return True


def create_image_url(user_id: int):
    url = f'{user_id}/{datetime.utcnow()}.jpg'.replace(':', '-')
    return url


def upload_file(temp_file: UploadFile, user_id: int, url: str):
    if is_validate_image_file(temp_file):
        if not os.path.exists(f'media/{user_id}'):
            os.mkdir(f'media/{user_id}')
        with open(f'media/{url}', 'wb') as file:
            copyfileobj(temp_file.file, file)
        return True


def delete_file(image_url):
    os.remove(f'media/{image_url}')
