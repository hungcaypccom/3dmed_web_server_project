from fastapi import APIRouter,Depends,Security

from app.schema import ResponseSchema, RegisterSchema, LoginSchema, ForgotPasswordSchema
from app.repository.auth_repo import JWTBearer, JWTRepo
from fastapi.security import HTTPAuthorizationCredentials
from app.service.user_service import UserService
from app.service import role_service

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

@router.get("/acc", response_model=ResponseSchema, response_model_exclude_none=True)
async def get_user_profile(credentials: HTTPAuthorizationCredentials = Security(JWTBearer())):
    token = JWTRepo.extract_token(credentials)
    r1 = await UserService.find_account(token['username'])
    print(r1.id)
    result = await role_service.find_role_by_user_id(r1.id)
    return ResponseSchema(detail="Successfully fetch data!", result=result)