from app.model import Person, Users, UsersRole, Role

from app.repository.users import UsersRepository
from sqlalchemy.future import select
from app.config import db

class UserService:

    async def find_account(account: str):
        info = await UsersRepository.find_by_username(account)
        return info

    async def find_account_all():
        info = await UsersRepository.get_all()
        return info

    @staticmethod
    async def get_user_profile_user(username):
        query = select(Users.username,
                       Users.password, 
                        Person.name, 
                        Person.Date_start,
                        Person.Date_end,
                        Person.profile,
                        Person.phone_number,
                        Person.adress
                        ).join_from(Users,Person).where(Users.username == username)
        return(await db.execute(query)).mappings().one()

