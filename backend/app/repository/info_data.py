
from multiprocessing import synchronize
from sqlalchemy import update as sql_update
from sqlalchemy.future import select
from sqlalchemy import update as sql_update, delete as sql_delete
from app.config import db, commit_rollback


from app.config import db, commit_rollback
from app.model.info_data import InfoData
from app.repository.base_repo import BaseRepo


class InfoDataRepository(BaseRepo):
    model = InfoData

    @staticmethod
    async def find_by_uploadTimeStr(uploadTimeStr: str):
        query = select(InfoData).where(InfoData.uploadTimeStr == uploadTimeStr)
        return (await db.execute(query)).scalar_one_or_none()
  

    @staticmethod
    async def find_by_user_id(user_id):
        query = select(InfoData).where(InfoData.user_id == user_id)
        return (await db.execute(query)).scalars().all()
    
    @staticmethod
    async def find_by_status(status):
        query = select(InfoData).where(InfoData.status == status)
        return (await db.execute(query)).scalars().all()
    

    @staticmethod
    async def delete_by_uploadTimeStr(uploadTimeStr: str):
        query = sql_delete(InfoData).where(InfoData.uploadTimeStr == uploadTimeStr)
        await db.execute(query)
        await commit_rollback()
    

    @staticmethod
    async def find_by_downloadable(downloadable):
        query = select(InfoData).where(InfoData.downloadable == downloadable)
        return (await db.execute(query)).scalars().all()
    
    @staticmethod
    async def update_status_downloadable(uploadTimeStr, status, downloadable):
        query = sql_update(InfoData).where(InfoData.uploadTimeStr == uploadTimeStr).values(
            status=status).values(downloadable=downloadable).execution_options(synchronize_session="fetch")
        await db.execute(query)
        await commit_rollback()

   