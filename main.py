import secrets
from typing import Annotated

import uvicorn
import contextlib

from fastapi import FastAPI, Depends, HTTPException, Header
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from starlette import status

from db.session import global_init

from src.users import router as users_router


@contextlib.asynccontextmanager
async def lifespan(application: FastAPI):
    await global_init()
    yield
    print('Shutdown')


security = HTTPBasic()
app = FastAPI(title="exe", version="0.0.1", lifespan=lifespan)


data = {"Admin": 'admin'}
tokens = {"fv4235kj287gn2ifo33jd9uh13ew": 'Admin'}


def auth_user(credentials: Annotated[HTTPBasicCredentials, Depends(security)]):
    unauthorized = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Invalid username or password',
        headers={'WWW-Autheticate': 'Basic'}
    )

    pwd = data.get(credentials.username, '')

    if credentials.username not in data:
        raise unauthorized

    if not secrets.compare_digest(credentials.password.encode('utf-8'), pwd.encode('utf-8')):
        raise unauthorized

    return credentials.username


def auth_user_by_token(static_token: str = Header(alias='x-auth-token')):
    if token := tokens.get(static_token):
        return token

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Invalid username or password',
        headers={'WWW-Autheticate': 'Basic'}
    )


@app.get('/login')
async def login(auth_username: str = Depends(auth_user)):
    return {'username': f'{auth_username}'}


app.include_router(users_router)


if __name__ == '__main__':
    uvicorn.run('main:app', host="localhost", port=8000, reload=True)
