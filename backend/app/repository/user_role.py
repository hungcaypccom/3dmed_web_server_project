from app.model.user_role import UsersRole
from app.repository.base_repo import BaseRepo
from typing import List
from sqlalchemy.future import select

from app.config import db,commit_rollback

class UsersRoleRepository(BaseRepo):
    model = UsersRole

    @staticmethod
    async def find_by_user_id(user_id:str):
        query = select(UsersRole).where(UsersRole.users_id == user_id)
        return (await db.execute(query)).scalar_one_or_none()
