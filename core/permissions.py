from dataclasses import dataclass
from fastapi import HTTPException
from sqlmodel import Session, SQLModel
from core.db import retrieve_instance_from_database
from core.settings import USER_MODEL, USER_FIELD


@dataclass
class IndirectDataOfOwner:
    relative_model: SQLModel
    relative_id: int


def permit_for_owner(owner_id: int, user_id: int):
    return True if owner_id == user_id else False


def permit_for_admin(user_id: int, session: Session):
    user = retrieve_instance_from_database(USER_MODEL, user_id, session)
    return True if user.is_admin else False


def permit_for_admin_or_owner(current_user_id: int, owner_id: int | IndirectDataOfOwner, session: Session):
    if isinstance(owner_id, IndirectDataOfOwner):
        owner_id = getattr(retrieve_instance_from_database(owner_id.relative_model, owner_id.relative_id, session),
                           USER_FIELD)
    if owner_id and permit_for_owner(owner_id, current_user_id):
        return True
    if permit_for_admin(current_user_id, session):
        return True
    else:
        raise HTTPException(400, detail='Not permitted')
