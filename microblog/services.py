import os
from shutil import copyfileobj
from datetime import datetime

from fastapi import UploadFile, HTTPException
from sqlmodel import Session

from core.db import (write_to_database, delete_from_database, retrieve_instance_from_database, update_in_database,
                     check_user_exists)
from core.permisions import permit_for_owner
from microblog.models import Image, CreateImage
from auth.models import User


# Методы CRUD операций
def retrieve_images(user_id: int, session: Session):
    user = retrieve_instance_from_database(User, user_id, session)
    if not user:
        raise HTTPException(401, detail='User is not exists')
    images = user.images
    return images


def retrieve_image(image_id: int, session: Session):
    image = retrieve_instance_from_database(Image, image_id, session)
    return image


@permit_for_owner
def create_image(temp_file: UploadFile, image: CreateImage, session: Session, current_user_id: int, user_id: int):
    if not check_user_exists(session, user_id=user_id):
        raise HTTPException(400, detail='User not found')
    url = create_image_url(user_id)
    if upload_file(temp_file, user_id, url):
        image = Image(url=url,
                      user=retrieve_instance_from_database(User, user_id, session),
                      **image.dict())
        write_to_database(image, session)
        return image


def delete_image(image_id: int, current_user_id: int, session: Session):
    if image := retrieve_instance_from_database(Image, image_id, session):
        delete_from_database(Image, image_id, session)
    delete_file(image.url)


def update_image(image_id: int, text: str, current_user_id: int, session: Session):
    if image := retrieve_instance_from_database(Image, image_id, session):
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
