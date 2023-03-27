from fastapi import APIRouter,Depends,Security

from app.schema import ResponseSchema, RegisterSchema, LoginSchema, ForgotPasswordSchema
from app.repository.auth_repo import JWTBearer, JWTRepo, JWTBearerAdmin
from fastapi.security import HTTPAuthorizationCredentials
from app.service.user_service import UserService
from app.service import role_service
from app.schema import ResponseSchema, RegisterSchema, LoginSchema, ForgotPasswordSchema
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

@router.post("/forgot-password", response_model=ResponseSchema, response_model_exclude_none=True)
async def forgot_password(request_body: ForgotPasswordSchema):
    await AuthService.forgot_password_service(request_body)
    return ResponseSchema(detail="Successfully update data!")

@router.get("/chage-status-infoData/{stt}")
async def chageStatusInfoData(stt):
    return await info_data_service.InFoDataService.update_status_downloadable(stt,False,False)

@router.get("/delete-infoData/{uploadTimeStr}")
async def deleteinfodata(uploadTimeStr):
    return await info_data_service.InFoDataService.delete_by_str()

@router.get("/find-infoData/{uploadTimeStr}")
async def findInfoData(uploadTimeStr):
    return await info_data_service.InFoDataService.find_by_str(uploadTimeStr)

@router.get("/find-by-status/{status}")
async def findstatus(status):
    return await info_data_service.InFoDataService.find_by_status(status)

@router.get("/get-all-account/")
async def getallaccount():
    return await UserService.find_account_all()