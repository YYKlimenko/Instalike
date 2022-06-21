from fastapi import FastAPI
from core.models import CreateImage
import services

app = FastAPI()


@app.get('/api/v1/{user_id}/')
def retrieve_images(user_id: int):
    response = services.get_images(user_id)
    return response


@app.post('/api/v1/{user_id}/')
def post_image(user_id: int, image: CreateImage):
    return services.post_image(user_id, image)


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
