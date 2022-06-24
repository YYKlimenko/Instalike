from fastapi import FastAPI, UploadFile
from core.models import CreateImage
import services

app = FastAPI()


@app.get('/api/v1/{user_id}/')
def retrieve_images(user_id: int):
    response = services.get_images(user_id)
    return response


@app.post('/api/v1/{user_id}/')
def post_image(user_id: int, file: UploadFile, image: CreateImage):
    url = services.get_image_url(user_id, file, image.date)
    if url:
        return services.post_image(user_id, url, image)
    else:
        return {'error': 'Файл не загружен'}


# @app.get('api/v1/{user_id}/{image_id}')
# async def get_image(user_id: int, image_id: int):
#     return services.get_image(user_id, image_id)
#
#
# @app.delete('api/v1/{user_id}/{image_id}')
# async def delete_image(user_id: int, image_id: int):
#     return services.delete_image(user_id, image_id)
#
#
# @app.update('api/v1/{user_id}/{image_id}')
# async def update_image(user_id: int, image_id: int):
#     return services.update_image(user_id, image_id)
