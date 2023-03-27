from fastapi import APIRouter,Depends,Security

from app.schema import ResponseSchema, RegisterSchema, LoginSchema, ForgotPasswordSchema
from app.repository.auth_repo import JWTBearer, JWTRepo, JWTBearerAdmin
from fastapi.security import HTTPAuthorizationCredentials
from app.service.user_service import UserService
from app.service.person_service import PersonService
from app.service import role_service
from app.schema import ResponseSchema, RegisterSchema, LoginSchema, ForgotPasswordSchema, UpdateSchema
from app.service.auth_service import AuthService
from app.service import info_data_service

router = APIRouter(
    prefix="/admin",
    tags=['admin'],
    dependencies=[Depends(JWTBearerAdmin())]
)


@router.post("/register", response_model=ResponseSchema, response_model_exclude_none=True)
async def register(request_body: RegisterSchema):
    await AuthService.register_service(request_body)
    return ResponseSchema(detail="Successfully save data!")

@router.post("/update_user_details", response_model=ResponseSchema, response_model_exclude_none=True)
async def register(request_body: UpdateSchema):
    await PersonService.update_person(request_body)
    return ResponseSchema(detail="Successfully save data!")

@router.post("/forgot-password", response_model=ResponseSchema, response_model_exclude_none=True)
async def forgot_password(request_body: ForgotPasswordSchema):
    await AuthService.forgot_password_service(request_body)
    return ResponseSchema(detail="Successfully update data!")

"""@router.get("/chage-status-infoData/{uploadTimeStr},{status:bool}, {downloadable:bool}")
async def chageStatusInfoData(stt):
    return await info_data_service.InFoDataService.update_status_downloadable()"""

@router.get("/delete-infoData/{uploadTimeStr}")
async def deleteinfodata(uploadTimeStr):
    return await info_data_service.InFoDataService.delete_by_str()

@router.get("/find-infoData/{uploadTimeStr}")
async def findInfoData(uploadTimeStr):
    return await info_data_service.InFoDataService.find_by_str(uploadTimeStr)

@router.get("/find-by-status/{status}")
async def findstatus(status):
    return await info_data_service.InFoDataService.find_by_status(status)

@router.get("/get-all-account")
async def getallaccount():
    return await UserService.find_account_all()

@router.get("/data-info-by-user/{username}")
async def datainfobyuser(username):
    result = await info_data_service.InFoDataService.find_by_user(username)
    return ResponseSchema(detail="Successfully fetch data!", result=result)

@router.get("/data-info-find-all")
async def datainfofindall():
    result = await info_data_service.InFoDataService.find_all()
    return ResponseSchema(detail="Successfully fetch data!", result=result)


@router.get("/user_details{username}", response_model=ResponseSchema, response_model_exclude_none=True)
async def get_user_profile(username):
    result = await UserService.get_user_profile_user(username)
    return ResponseSchema(detail="Successfully fetch data!", result=result)


"""@router.get("/user_details_all")
async def get_user_profile_all():
    return await UserService.find_account_all()
    return accounts
    results = []
    for account in accounts:
        result = await UserService.get_user_profile_user(["username"])
        results.append(result)
    return ResponseSchema(detail="Successfully fetch data!", result=results)"""

@router.get("/user_all")
async def getallaccount():
    accounts = await UserService.find_account_all()
    results = []
    for account in accounts:
        result = await UserService.get_user_profile_user(account.username)
        results.append(result)
    return ResponseSchema(detail="Successfully fetch data!", result=results)