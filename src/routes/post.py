from fastapi import APIRouter
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext

router = APIRouter(prefix='/post')


@router.get("/")
async def ping():
    return {"Hello": "World"}