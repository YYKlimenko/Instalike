from sqlmodel import Session
from core.models import Image
from core.db import engine


def get_images(user_id: int):
    print(engine.url)
    with Session(engine) as session:
        results = session.query(Image).filter(Image.user_id == user_id)
        return results.all()


def post_image(user_id: int, image: Image):
    with Session(engine) as session:
        image = Image(**image.dict(), user_id=user_id)
        session.add(image)
        session.commit()
        session.refresh(image)
        return image
