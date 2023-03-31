from fastapi import APIRouter,Depends,Security, Response, Body

from app.schema import ResponseSchema, UpdateUserSchema, DeleteDataListSchema
from app.repository.auth_repo import JWTBearer, JWTRepo
from fastapi.security import HTTPAuthorizationCredentials
from app.service.user_service import UserService
from app.service import  info_data_service, person_service

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

@router.post("/edit-profile", response_model=ResponseSchema, response_model_exclude_none=True)
async def edit_profile(request_body: UpdateUserSchema, credentials: HTTPAuthorizationCredentials = Security(JWTBearer())):
    token = JWTRepo.extract_token(credentials)
    await person_service.PersonService.update_person_user(request_body, token["username"])
    return ResponseSchema(detail="Successfully update data!")

@router.post("/download-file")
async def download_file(response: Response, uploadTimeStr: str = Body(...)):
    return await client_download.client_download_file(Response, uploadTimeStr)
    
@router.get("/data-info-total-count",response_model=ResponseSchema, response_model_exclude_none=True)
async def data_info_total_count(downloadable:bool, credentials: HTTPAuthorizationCredentials = Security(JWTBearer())):
    token = JWTRepo.extract_token(credentials)
    result = await info_data_service.InFoDataService.find_by_user_total_count(token['username'], downloadable)
    return ResponseSchema(detail="Successfully fetch data!", result=result)
    
@router.get("/data-info-pagging",response_model=ResponseSchema, response_model_exclude_none=True)
async def data_info_pagging(downloadable:bool, page:int, count:int, credentials: HTTPAuthorizationCredentials = Security(JWTBearer()) ):
    token = JWTRepo.extract_token(credentials)
    result = await info_data_service.InFoDataService.find_by_user_pagging(token['username'], page, count, downloadable)
    return ResponseSchema(detail="Successfully fetch data!", result=result)

@router.post("/delete-file")
async def delete_file(response: Response, datalist: list[str]):
    result = await client_download.client_delete_file(datalist)
    return ResponseSchema(detail="Successfully", result=result)
