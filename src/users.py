from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from db.tables import User
from db.session import create_session

from src.schemas import UserModel


router = APIRouter(prefix='/users')


@router.post("/")
async def create_user(form: UserModel, session: AsyncSession = Depends(create_session)):
    """TODO: Crypt password"""

    exists = await session.execute(select(User).where(User.login == form.login))

    if exists.scalar_one_or_none() is not None:
        raise HTTPException(status_code=400, detail="login already registered")

    user = User(login=form.login, email=form.email, password=form.password)
    session.add(user)
    await session.commit()
    return {'msg': f'{user}'}


@router.get("/{login}")
async def get_user(login: str, session: AsyncSession = Depends(create_session)):
    result = await session.execute(select(User).where(User.login == login))
    user = result.scalar_one_or_none()

    if user is None:
        raise HTTPException(status_code=404, detail="user not found")

    return {'msg': f'{user}'}