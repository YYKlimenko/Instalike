from sqlmodel import Session, select
from core.db import engine
from core.models import Image


def get_images():
    with Session(engine) as session:
        results = session.exec(select(Image)).first()
        print(results)
        return results


# def post_image(user_id, image: Image):
#     with Session(engine) as session:
#         session.add(Image(user_id=user_id, url=image.url, text=image.text))
#         session.commit()
#         return session.exec(select(Image).where(Image.user_id == image.user_id)).first()
        