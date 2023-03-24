import aiohttp
import aiofiles
import asyncio
import time
from fastapi import FastAPI
import pickle
import time

class Config:

    URL_login = "http://47.243.175.209:8080/EX-PRO/accLogin"
    URL_reset = "http://47.243.175.209:8080/EX-PRO/resetPwd"
    URL_getFileInfo = "http://47.243.175.209:8080/EX-PRO/api/file/getFileInfos"
    URL_download = "http://47.243.175.209:8080/EX-PRO/api/file/download"
    URL_cookies = "http://47.243.175.209:8080/EX-PRO"

    params = {
    "loginPwd": "loginPwd",
    "accountNo": "accountNo",
    "accessSource": "accessSource",
    "initPwd": "initPwd",
    "uploadTimeStr": "uploadTimeStr"
    }

    loginAccount = {
        "account": "994985849",
        "password": "d33314f30983215c29c2af0c1bcd2b43",
        "accessSource": "pc"
    }

