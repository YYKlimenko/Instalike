from fastapi import APIRouter, Depends, Response, UploadFile
from microblog.models import CreateImage
import microblog.services as services
from auth.services import handle_auth


microblog = APIRouter()


@microblog.get('/api/v1/{user_id}/',
               status_code=200,
               tags=['images'],
               description='Retrieve all images by user')
def get_images(user_id: int):
    return services.retrieve_images(user_id)


@microblog.post('/api/v1/{user_id}/',
                status_code=201,
                tags=['images'],
                description='Create new image')
def post_image(user_id: int, file: UploadFile, image: CreateImage = Depends(), token: str = Depends(handle_auth)):
    return services.create_image(user_id, file, image, token['sub'])


@microblog.get('/api/v1/images/{image_id}/',
               status_code=200,
               tags=['images'],
               description='Retrieve image by ID')
def get_image(image_id: int):
    return services.retrieve_image(image_id)


@microblog.delete('/api/v1/images/{image_id}/',
                  status_code=204,
                  response_class=Response,
                  tags=['images'],
                  description='Delete image')
def delete_image(image_id: int, token: str = Depends(handle_auth)):
    services.delete_image(image_id, token['sub'])


@microblog.put('/api/v1/{image_id}',
               status_code=201,
               tags=['images'],
               description='Change description of image')
def update_image(image_id: int, text: str, token: str = Depends(handle_auth)):
    return services.update_image(image_id, text, token['sub'])
