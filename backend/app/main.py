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
        #await AuthService.register_service(admin_reg)
        task1 = asyncio.create_task(auto_compare())
        task2 = asyncio.create_task(auto_download())
        asyncio.gather(task1, task2)
       

        

    @app.on_event("shutdown")
    async def shutdown():
        await db.close()

    from app.controller import authentication, users, admin

    app.include_router(authentication.router)
    app.include_router(users.router)
    app.include_router(admin.router)
    return app
    


app = init_app()

"""@router.get("/role")
async def role():
    await auth_service.generate_role()
    return("welcome home")


@router.get("/name")
async def role(): 
    return await info_data_service.InFoDataService.find_by_user("225678373")
    
@router.get("/all")
async def role(): 
    return await info_data_service.InFoDataService.find_by_user()

@router.get("/userall")
async def role(): 
    re = await user_service.find_account_all()
    print(re[0].username)
    return re



# test hans3d
@router.get("/cookies")
async def f():
   await han3d_service.Service.takeCookies()


@router.get("/reset")
async def f():
    return await han3d_service.Service.reset(5)

@router.get("/login")
async def f():
   return await han3d_service.Service.login(5)

@router.get("/getFileInfo")
async def f():
   re = await han3d_service.Service.getInfoData("994985849", 5)
   re1 = re["data"]
   for re2 in re1:
       print(re2["uploadTimeStr"])
   return re1

@router.get("/download")
async def f():
   return await han3d_service.Service.download("20200829142930990", "994985849", 50)
async def role(): 
    return await user_service.find_account_all()

@router.get("/deleteperson")
async def f():
    return await person_service.PersonService.delete_all_person()

@router.get("/sync")
async def f():
    return await AutoDownloadService.sync_infoData()

@router.get("/downloaddata")
async def f():
    return await AutoDownloadService.download()

@router.get("/deleteinfodata")
async def f():
    return await info_data_service.InFoDataService.delete_by_str("20221212172841377")
app.include_router(router)

@router.get("/findinfodata")
async def f():
    return await info_data_service.InFoDataService.find_by_str("20221212172841377")

@router.get("/findstatus")
async def f():
    return await info_data_service.InFoDataService.find_by_status(True)

@router.get("/updatestatus")
async def f():
    return await info_data_service.InFoDataService.update_status_downloadable("20221212172841377",True,True)

# test autodownload
@router.get("/autologin")
async def f():
    return await AutoDownloadService.auto_login()"""


"""#test autodownload
@router.get("/test")
async def f():
    return await AuthService.register_service(admin)
"""
app.include_router(router)


# test dtbase



def start():
    #Lauched with 'poetry run start' at root level
    uvicorn.run("app.main:app", host="localhost", port=8888, reload=True)