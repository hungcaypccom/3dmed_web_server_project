from app.repository.person import PersonRepository
from app.schema import UpdateSchema
from app.model.users import Users
from app.model.person import Person
from sqlalchemy.future import select
from app.config import db
from datetime import datetime, date

class PersonService:
    
    @staticmethod
    async def delete_all_person():
        return await PersonRepository.delete_all()
    
    @staticmethod
    async def update_person(register: UpdateSchema):
        query = select(Person.id
                        ).join_from(Users,Person).where(Users.username == register.username)
        _person_id =  (await db.execute(query)).scalar_one_or_none()

        print(_person_id)
        Date_start = datetime.strptime(register.Date_start, '%d-%m-%Y')
        Date_end = datetime.strptime(register.Date_end, '%d-%m-%Y')
        _person = Person(id=_person_id, name=register.name, Date_start=Date_start, 
    Date_end=Date_end, profile=register.profile, phone_number=register.phone_number, adress=register.adress)
        
        await PersonRepository.update(_person_id,**_person.dict())
    

 

