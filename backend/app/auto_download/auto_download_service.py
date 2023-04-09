from app.auto_download import function, config
from app.hans3d.han3d_service import Service
from app.service import info_data_service
import asyncio


class AutoDownloadService:

    @staticmethod
    async def auto_login():
        status = await Service.login(config.timeout_request_data)
        if status["status"] == 2002:
            await Service.reset(config.timeout_request_data)
            await Service.takeCookies()
            return await Service.login(config.timeout_request_data)

    @staticmethod
    async def sync_infoData():
        try:
            accounts = await function.Function.get_all_account()
            tasks = []
            for account in accounts:
                print(f'{account.username}')
                task = asyncio.create_task(function.Function.sync_infoData(account.username, config.timeout_request_data*len(accounts)))
                tasks.append(task)
            await asyncio.gather(*tasks)
        except Exception as e:
            print("Error occurred: ", e)
        
    @staticmethod
    async def download():
        try:
            downloads = await function.Function.find_infoData_by_status(False)
            for download in downloads:
                if await function.Function.download_by_uploadTimeStr(download.uploadTimeStr, download.accountNo, config.timeout_download_data):
                    await info_data_service.InFoDataService.update_status_downloadable(download.uploadTimeStr,True,True)
        except Exception as e:
                print("Error occurred: ", e)
   
            



            