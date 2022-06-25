from datetime import datetime
from fastapi import FastAPI, Depends, Response, UploadFile
from core.models import CreateImage
import microblog.services as services

app = FastAPI()


@app.get('/api/v1/{user_id}/', status_code=201)
def retrieve_images(user_id: int):
    response = services.get_images(user_id)
    return response


@app.post('/api/v1/{user_id}/', status_code=201)
def post_image(user_id: int, file: UploadFile, image: CreateImage = Depends()):
    url: str = services.get_image_url(user_id, file, datetime.utcnow())
    if url:
        return services.post_image(user_id, url, image)
    else:
        return {'error': 'Файл не загружен'}


@app.get('/api/v1/images/{image_id}/', status_code=200)
def get_image(image_id: int):
    return services.get_image(image_id)


@app.delete('/api/v1/images/{image_id}/', status_code=204, response_class=Response)
def delete_image(image_id: int):
    services.delete_image(image_id)


@app.put('/api/v1/{image_id}', status_code=201)
def update_image(image_id: int, text: str):
    return services.update_image(image_id, text)
