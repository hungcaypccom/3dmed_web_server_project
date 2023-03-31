from fastapi import APIRouter,Depends,Security, Response
from app.client_download import client_download
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

@router.post("/update-user-details", response_model=ResponseSchema, response_model_exclude_none=True)
async def register(request_body: UpdateSchema):
    await PersonService.update_person(request_body)
    return ResponseSchema(detail="Successfully save data!")

@router.post("/forgot-password", response_model=ResponseSchema, response_model_exclude_none=True)
async def forgot_password(request_body: ForgotPasswordSchema):
    await AuthService.forgot_password_service(request_body)
    return ResponseSchema(detail="Successfully update data!")

@router.post("/chage-status-infoData")
async def chageStatusInfoData(uploadTimeStr,status:bool ,downloadable:bool):
    await info_data_service.InFoDataService.update_status_downloadable(uploadTimeStr, status, downloadable)
    return ResponseSchema(detail="Successfully update!")

@router.post("/delete-infoData")
async def deleteinfodata(uploadTimeStr):
    return await info_data_service.InFoDataService.delete_by_str()

@router.post("/find-infoData")
async def findInfoData(uploadTimeStr):
    return await info_data_service.InFoDataService.find_by_str(uploadTimeStr)

@router.get("/find-info-data-by-status")
async def findstatus(status:bool):
    return await info_data_service.InFoDataService.find_by_status(status)

@router.get("/find-info-data-by-downloadable")
async def findstatus(downloadable:bool):
    return await info_data_service.InFoDataService.find_by_downloadable(downloadable)

@router.get("/get-all-account")
async def getallaccount():
    return await UserService.find_account_all()


@router.post("/update-data-info-by-user")
async def updatedatainfobyuser(username, status:bool, downloadable: bool):
    results = await info_data_service.InFoDataService.find_by_user(username)
    for result in results:
        await info_data_service.InFoDataService.update_status_downloadable(result.uploadTimeStr, status, downloadable)
    return ResponseSchema(detail="Successfully update!")


@router.get("/data-info-find-all")
async def datainfofindall():
    result = await info_data_service.InFoDataService.find_all()
    return ResponseSchema(detail="Successfully fetch data!", result=result)


@router.get("/user_details", response_model=ResponseSchema, response_model_exclude_none=True)
async def get_user_profile(username):
    result = await UserService.get_user_profile_user(username)
    return ResponseSchema(detail="Successfully fetch data!", result=result)



@router.get("/user_all")
async def getallaccount():
    accounts = await UserService.find_account_all()
    results = []
    for account in accounts:
        result = await UserService.get_user_profile_user(account.username)
        results.append(result)
    return ResponseSchema(detail="Successfully fetch data!", result=results)

@router.post("/delete-file")
async def delete_file(response: Response, datalist: list[str]):
    result = await client_download.client_delete_file(datalist)
    return ResponseSchema(detail="Successfully", result=result)


@router.get("/data-info-total-count",response_model=ResponseSchema, response_model_exclude_none=True)
async def data_info_total_count(downloadable:bool, username):
    result = await info_data_service.InFoDataService.find_by_user_total_count(username, downloadable)
    return ResponseSchema(detail="Successfully fetch data!", result=result)
    
@router.get("/data-info-pagging",response_model=ResponseSchema, response_model_exclude_none=True)
async def data_info_pagging(downloadable:bool, page:int, count:int, username ):
    result = await info_data_service.InFoDataService.find_by_user_pagging(username, page, count, downloadable)
    return ResponseSchema(detail="Successfully fetch data!", result=result)