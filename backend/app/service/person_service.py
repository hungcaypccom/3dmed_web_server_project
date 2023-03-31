from app.repository.person import PersonRepository
from app.repository.users import UsersRepository
from app.schema import UpdateSchema, UpdateUserSchema
from app.model.users import Users
from app.model.person import Person
from sqlalchemy.future import select
from app.config import db
from datetime import datetime, date
from fastapi import HTTPException
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class PersonService:
    
    @staticmethod
    async def delete_all_person():
        return await PersonRepository.delete_all()
    
    @staticmethod
    async def update_person(register: UpdateSchema):
        _username = await UsersRepository.find_by_username(register.username)
        if _username is None:
            raise HTTPException(status_code=404, detail="username !")
        query = select(Person.id
                        ).join_from(Users,Person).where(Users.username == register.username)
        _person_id =  (await db.execute(query)).scalar_one_or_none()

        Date_start = datetime.strptime(register.Date_start, '%d-%m-%Y')
        Date_end = datetime.strptime(register.Date_end, '%d-%m-%Y')
        _person = Person(id=_person_id, name=register.name, Date_start=Date_start, 
    Date_end=Date_end, profile=register.profile, phone_number=register.phone_number, adress=register.adress)
        
        await PersonRepository.update(_person_id,**_person.dict())
    

    @staticmethod
    async def update_person_user(register: UpdateUserSchema, username):
        _username = await UsersRepository.find_by_username(username)
        if  pwd_context.verify(register.old_password, _username.password):
            query = select(Person
                        ).join_from(Users,Person).where(Users.username == username)
            _person =  (await db.execute(query)).scalar_one_or_none()

            Date_start = _person.Date_start
            Date_end = _person.Date_end
            _person = Person(id=_person.id, name=register.name, Date_start=Date_start, 
            Date_end=Date_end, profile=register.profile, phone_number=register.phone_number, adress=register.adress)
            await UsersRepository.update_password(username, pwd_context.hash(register.new_password))
            await PersonRepository.update(_person.id,**_person.dict())
        else:
            raise HTTPException(status_code=400, detail="Invalid old password")