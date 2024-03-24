import uvicorn
import contextlib

from fastapi import FastAPI, Depends, HTTPException

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from db.tables import User
from db.session import global_init, create_session
from src.schemas import UserModel


@contextlib.asynccontextmanager
async def lifespan(application: FastAPI):
    await global_init()
    yield
    print('Shutdown')


app = FastAPI(title="exe", version="0.0.1", lifespan=lifespan)


@app.post("/")
async def create_user(form: UserModel, session: AsyncSession = Depends(create_session)):
    """TODO: Crypt password"""

    exists = await session.execute(select(User).where(User.login == form.login))

    if exists.scalar_one_or_none() is not None:
        raise HTTPException(status_code=400, detail="login already registered")

    user = User(login=form.login, email=form.email, password=form.password)
    session.add(user)
    await session.commit()
    return {'msg': f'{user}'}


@app.get("/{login}")
async def get_user(login: str, session: AsyncSession = Depends(create_session)):
    result = await session.execute(select(User).where(User.login == login))
    user = result.scalar_one_or_none()

    if user is None:
        raise HTTPException(status_code=404, detail="user not found")

    return {'msg': f'{user}'}


if __name__ == '__main__':
    uvicorn.run('main:app', host="localhost", port=8000, reload=True)
