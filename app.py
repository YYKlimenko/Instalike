from fastapi import FastAPI
from core.models import Image
import services


app = FastAPI()


@app.get('/', response_model=Image)
def get_images():
    response = services.get_images()
    return response


# @app.post('/api/v1/{user_id}/', response_model=Image)
# def post_image(user_id: int, image: Image):
#     return services.post_image(user_id, image)


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
