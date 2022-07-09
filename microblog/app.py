from fastapi import APIRouter, Depends, Response, UploadFile
from sqlmodel import Session
from core.db import get_session
from core.permissions import permit_for_admin_or_owner, IndirectDataOfOwner
from microblog.models import Image, CreateImage
from auth.services import handle_auth
import microblog.services as services


microblog = APIRouter(tags=['Images'])


@microblog.get('/api/v1/{user_id}/',
               status_code=200,
               description='Retrieve all images by user')
def get_images(user_id: int, session: Session = Depends(get_session)):
    return services.retrieve_images(user_id, session)


@microblog.post('/api/v1/{user_id}/',
                status_code=201,
                description='Create new image')
def post_image(file: UploadFile, image: CreateImage = Depends(), token: str = Depends(handle_auth),
               session: Session = Depends(get_session)):
    return services.create_image(file, image, session, user_id=token['sub'])


@microblog.get('/api/v1/images/{image_id}/',
               status_code=200,
               description='Retrieve image by ID')
def get_image(image_id: int, session: Session = Depends(get_session)):
    return services.retrieve_image(image_id, session)


@microblog.delete('/api/v1/images/{image_id}/',
                  status_code=204,
                  response_class=Response,
                  description='Delete image')
def delete_image(image_id: int, token: str = Depends(handle_auth), session: Session = Depends(get_session)):
    permit_for_admin_or_owner(token['sub'], IndirectDataOfOwner(Image, image_id), session)
    services.delete_image(image_id, token['sub'], session)


@microblog.put('/api/v1/{image_id}',
               status_code=201,
               description='Change description of image')
def update_image(image_id: int, text: str, token: str = Depends(handle_auth), session: Session = Depends(get_session)):
    permit_for_admin_or_owner(token['sub'], IndirectDataOfOwner(Image, image_id), session)
    return services.update_image(image_id, text, session)
