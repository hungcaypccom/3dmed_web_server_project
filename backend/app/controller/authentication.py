from fastapi import APIRouter

from app.schema import ResponseSchema, RegisterSchema, LoginSchema, ForgotPasswordSchema
from app.service.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=['Authentication'])



@router.post("/login", response_model=ResponseSchema)
async def login(requset_body: LoginSchema):
    token = await AuthService.logins_service(requset_body)
    return ResponseSchema(detail="Successfully login", result={"token_type": "Bearer", "access_token": token})

@router.post("/admin", response_model=ResponseSchema)
async def login(requset_body: LoginSchema):
    token = await AuthService.logins_service_admin(requset_body)
    return ResponseSchema(detail="Successfully login", result={"token_type": "Bearer", "access_token": token})


