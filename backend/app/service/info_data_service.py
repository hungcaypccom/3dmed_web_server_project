import base64
from datetime import datetime
from uuid import uuid4
from fastapi import HTTPException

from app.model import Person, Users, UsersRole, Role, InfoData
from app.repository.role import RoleRepository
from app.repository.users import UsersRepository
from app.repository.person import PersonRepository
from app.repository.user_role import UsersRoleRepository
from app.repository.info_data import InfoDataRepository
from app.service.user_service import UserService
class InFoDataService:

    @staticmethod
    async def write_data(data, username:str):

        # Create uuid
        _infoData_id = str(uuid4())
        _username = await UsersRepository.find_by_username(username)
        # mapping request data to class entity table
        _infoData = InfoData(id=_infoData_id, accountNo=data["accountNo"], uploadTimeStr=data["uploadTimeStr"], 
                    fileSize=data["fileSize"], createTime=data["createTime"], name=data["name"], 
                    birthday=data["birthday"], phone=data["phone"],sex=data["sex"], status=data["status"],downloadable=data["downloadable"], user_id=_username.id, userIF=_username)

             #  insert to tables
        await InfoDataRepository.create(**_infoData.dict())

    @staticmethod
    async def find_by_user(account: str):
        acc = await UserService.find_account(account)
        return await InfoDataRepository.find_by_user_id(acc.id)
    
    @staticmethod  
    async def find_all():
        return await InfoDataRepository.get_all()
    
    @staticmethod  
    async def find_by_str(str):
        return await InfoDataRepository.find_by_uploadTimeStr(str)
    
    @staticmethod  
    async def find_by_status(status):
        return await InfoDataRepository.find_by_status(status)
    
    @staticmethod  
    async def delete_by_str(uploadTimeStr):
        return await InfoDataRepository.delete_by_uploadTimeStr(uploadTimeStr)
    
    @staticmethod  
    async def update_status_downloadable(uploadTimeStr, status, downloadable):
        return await InfoDataRepository.update_status_downloadable(uploadTimeStr, status, downloadable)