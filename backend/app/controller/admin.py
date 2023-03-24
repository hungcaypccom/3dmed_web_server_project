from fastapi import APIRouter,Depends,Security

from app.schema import ResponseSchema, RegisterSchema, LoginSchema, ForgotPasswordSchema
from app.repository.auth_repo import JWTBearer, JWTRepo, JWTBearerAdmin
from fastapi.security import HTTPAuthorizationCredentials
from app.service.user_service import UserService
from app.service import role_service
from app.schema import ResponseSchema, RegisterSchema, LoginSchema, ForgotPasswordSchema
from app.service.auth_service import AuthService

router = APIRouter(
    prefix="/admin",
    tags=['admin'],
    dependencies=[Depends(JWTBearerAdmin())]
)

@router.get("/acc", response_model=ResponseSchema, response_model_exclude_none=True)
async def get_user_profile(credentials: HTTPAuthorizationCredentials = Security(JWTBearerAdmin())):
    token = JWTRepo.extract_token(credentials)
    r1 = await UserService.find_account(token['username'])
    print(r1.id)
    result = await role_service.find_role_by_user_id(r1.id)
    return ResponseSchema(detail="Successfully fetch data!", result=result)

@router.post("/register", response_model=ResponseSchema, response_model_exclude_none=True)
async def register(request_body: RegisterSchema):
    await AuthService.register_service(request_body)
    return ResponseSchema(detail="Successfully save data!")