import uvicorn
from fastapi import FastAPI, APIRouter
from app.config import db
from app.service import auth_service, user_service, role_service, info_data_service, person_service
from app.hans3d import han3d_service
from app.auto_download.auto_download_service import AutoDownloadService
from app.auto_download import config as AutoDownloadConfig
from datetime import date
from app.service.auth_service import AuthService
from app.schema import RegisterSchema
from app.client_download import client_download
import time
import asyncio
from pathlib import Path
from fastapi import HTTPException
from fastapi import FastAPI, Response, status


from fastapi import FastAPI
from aiohttp import web
from app.client_download import config


router = APIRouter()
import json

admin_reg = RegisterSchema(
    username= "admin",
    password= "admin",
    name= "admin2",
    Date_start= "23-01-2023",
    Date_end= "23-10-2023",
    profile= "str",
    phone_number= "str",
    adress= "str",
    role= "admin"
)

datafolder = "datas"
name= "20221212172841377"

async def auto_compare():
    while True:
        await AutoDownloadService.auto_login()
        await AutoDownloadService.sync_infoData()
        await asyncio.sleep(AutoDownloadConfig.interval_compare_infoData) 

async def auto_download():
    while True:
        await AutoDownloadService.download()
        await asyncio.sleep(AutoDownloadConfig.interval_download) 
        

def init_app():
    db.init()

    app = FastAPI(
        title="Minh Hung",
        description="Login Page",
        version="1"
    )

    @app.on_event("startup")
    async def startup():
        await db.create_all()
        await AuthService.generate_role()

        #uncomment below line for the first time running - tocreate admin account
        #await AuthService.register_service(admin_reg)

        """
        - 3 lines below to run auto download from hans's server
        - when creating admin account for the first time  please comment 3 lines belows
        - after created admin account, uncommnent 3 lines belows and comment the line above to not creating admin account
        - then restart running server """

        #task1 = asyncio.create_task(auto_compare())
        #task2 = asyncio.create_task(auto_download())
        #asyncio.gather(task1, task2)"""
       

        

    @app.on_event("shutdown")
    async def shutdown():
        await db.close()

    from app.controller import authentication, users, admin

    app.include_router(authentication.router)
    app.include_router(users.router)
    app.include_router(admin.router)
    return app
    


app = init_app()
app.include_router(router)

def start():
    #Lauched with 'poetry run start' at root level
    uvicorn.run("app.main:app", host="localhost", port=8888, reload=True)