import os
from shutil import copyfileobj
from datetime import datetime

from fastapi import UploadFile

from core.db import (write_to_database, delete_from_database, retrieve_instance_from_database, update_in_database,
                     retrieve_from_database_by_user)
from microblog.models import Image, CreateImage
from auth.models import User


# Методы CRUD операций
def retrieve_images(user_id: int):
    return retrieve_from_database_by_user(Image, user_id)


def retrieve_image(image_id: int):
    image = retrieve_instance_from_database(Image, image_id)
    return image


def create_image(user_id: int, temp_file: UploadFile, image: CreateImage):
    url = create_image_url(user_id)
    if upload_file(temp_file, user_id, url):
        image = Image(url=url,
                      user_id=retrieve_instance_from_database(User, user_id).id,
                      **image.dict(),
                      user=retrieve_instance_from_database(User, user_id))
        print(image)
        return write_to_database(image)


def delete_image(image_id):
    image = retrieve_image(image_id)
    delete_from_database(Image, image_id)
    delete_file(image.url)


def update_image(image_id, text):
    return update_in_database(Image, image_id, data={'text': text})


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

# import os
# from shutil import copyfileobj
# from datetime import datetime
# from fastapi import UploadFile
# from core.db import (
#     write_to_database, delete_from_database, retrieve_from_database, retrieve_from_database_by_user,
#     update_in_database
# )
# from microblog.models import Image
#
#
# # Методы CRUD операций
# def retrieve_images(user_id: int):
#     images = retrieve_from_database_by_user(Image, user_id)
#     return images
#
#
# def retrieve_image(image_id: int):
#     image = retrieve_from_database(Image, image_id)
#     return image
#
#
# def create_image(user_id: int, url: str, image: Image):
#     image = Image(user_id=user_id, url=url, **image.dict())
#     return write_to_database(image)
#
#
# def delete_image(image_id):
#     image = retrieve_image(image_id)
#     delete_from_database(Image, image_id)
#     delete_file(image.url)
#
#
# def update_image(image_id, text):
#     return update_in_database(Image, image_id, data={'text': text})
#
#
# #Методы работы с файлами
# def is_validate_image_file(file: UploadFile):
#     if file.content_type == 'image/jpeg':
#         return True
#
#
# def is_upload_file(url: str, user_id: int, temp_file: UploadFile):
#     if is_validate_image_file(temp_file):
#         if not os.path.exists(f'media/{user_id}'):
#             os.mkdir(f'media/{user_id}')
#         with open(f'media/{url}', 'wb') as file:
#             copyfileobj(temp_file.file, file)
#         return True
#     else:
#         return False
#
#
# def get_image_url(user_id: int, file: UploadFile, date: datetime):
#     url = f'{user_id}/{date}.jpg'.replace(':', '-')
#     if is_upload_file(url, user_id, file):
#         return url
#
#
# def delete_file(image_url):
#     os.remove(f'media/{image_url}')
