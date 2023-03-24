import uvicorn
from fastapi import FastAPI, APIRouter
from app.config import db
from app.service import auth_service, user_service, role_service, info_data_service, person_service
from app.hans3d import han3d_service
from app.auto_download.auto_download_service import AutoDownloadService
from datetime import date

router = APIRouter()
import json



roles = ["user", "admin"]




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



app.include_router(router)


# test dtbase



def start():
    #Lauched with 'poetry run start' at root level
    uvicorn.run("app.main:app", host="localhost", port=8888, reload=True)