from app.service.info_data_service import InFoDataService
from app.hans3d.han3d_service import Service
from app.service.user_service import UserService
from app.model import Person, Users, UsersRole, Role
class Function:
    
    @staticmethod
    async def find_infoData_by_account(account:str):
        return await InFoDataService.find_by_user(account)
    
    @staticmethod
    async def find_infoData_by_status(status):
        return await InFoDataService.find_by_status(status)
    
    @staticmethod
    async def get_file_info_by_account(account: str, timeout):
        return await Service.getInfoData(account, timeout=timeout)
    
    @staticmethod
    async def get_all_account():
        return await  UserService.find_account_all()
    
    @staticmethod
    async def write_infoData_by_account(data, account:str):
        return await InFoDataService.write_data(data, account)
    @staticmethod
    async def download_by_uploadTimeStr(uploadTimeStr:str, account, timeout):
        return await Service.download(uploadTimeStr, account, timeout)

    @staticmethod
    async def sync_infoData(account:str, timeout):
        getInfoData = await Function.get_file_info_by_account(account, timeout)
        infoDatas = getInfoData["data"]
        infoDataBase = await Function.find_infoData_by_account(account)
        if not infoDataBase:
            for infoData in infoDatas:
                data = {
                    "accountNo" : infoData["accountNo"], 
                    "uploadTimeStr" : infoData["uploadTimeStr"], 
                    "fileSize" : infoData["fileSize"], 
                    "createTime" : infoData["createTime"], 
                    "name" : infoData["name"], 
                    "birthday" : infoData["birthday"], 
                    "phone" : infoData["phone"], 
                    "sex" : infoData["sex"],
                    "status": True,
                    "downloadable": False
                }
                await Function.write_infoData_by_account(data = data, account= account)
        else:
            lastInfoData = (infoDatas[-1])
            lastInfoDataBase = infoDataBase[-1]
            if(lastInfoData["uploadTimeStr"]!=lastInfoDataBase.uploadTimeStr): 
                dataUpdate = {
                    "accountNo" : lastInfoData["accountNo"], 
                    "uploadTimeStr" : lastInfoData["uploadTimeStr"], 
                    "fileSize" : lastInfoData["fileSize"], 
                    "createTime" : lastInfoData["createTime"], 
                    "name" : lastInfoData["name"], 
                    "birthday" : lastInfoData["birthday"], 
                    "phone" : lastInfoData["phone"], 
                    "sex" : lastInfoData["sex"],
                    "status": False,
                    "downloadable": True
                }
                await Function.write_infoData_by_account(data = dataUpdate, account= account)
            else:
                print ("khong download gi ca")
           

       


 
                
              #  if await Function.download_by_uploadTimeStr((infoDatas[-1])["uploadTimeStr"], account, timeout):
                  