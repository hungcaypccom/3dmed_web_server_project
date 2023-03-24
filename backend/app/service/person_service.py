from app.repository.person import PersonRepository

class PersonService:
    
    @staticmethod
    async def delete_all_person():
        return await PersonRepository.delete_all()