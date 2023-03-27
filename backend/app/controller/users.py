from fastapi import APIRouter,Depends,Security, Response

from app.schema import ResponseSchema, RegisterSchema, LoginSchema, ForgotPasswordSchema
from app.repository.auth_repo import JWTBearer, JWTRepo
from fastapi.security import HTTPAuthorizationCredentials
from app.service.user_service import UserService
from app.service import role_service, auth_service, info_data_service
from app.client_download import client_download


router = APIRouter(
    prefix="/users",
    tags=['user'],
    dependencies=[Depends(JWTBearer())]
)


@router.get("/", response_model=ResponseSchema, response_model_exclude_none=True)
async def get_user_profile(credentials: HTTPAuthorizationCredentials = Security(JWTBearer())):
    token = JWTRepo.extract_token(credentials)
    result = await UserService.get_user_profile_user(token['username'])
    return ResponseSchema(detail="Successfully fetch data!", result=result)

@router.get("/data-info", response_model=ResponseSchema, response_model_exclude_none=True)
async def get_data_info(credentials: HTTPAuthorizationCredentials = Security(JWTBearer())):
    token = JWTRepo.extract_token(credentials)
    result = await info_data_service.InFoDataService.find_by_user(token['username'])
    return ResponseSchema(detail="Successfully fetch data!", result=result)

@router.post("/forgot-password", response_model=ResponseSchema, response_model_exclude_none=True)
async def forgot_password(request_body: ForgotPasswordSchema):
    await auth_service.AuthService.forgot_password_service(request_body)
    return ResponseSchema(detail="Successfully update data!")

@router.get("/download-file/{uploadTimeStr}")
async def download_file(response: Response, uploadTimeStr):
   return await client_download.client_download_file(Response, uploadTimeStr)

