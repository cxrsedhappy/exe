from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.schemas import UserCreateModel
from src.session import create_session
from src.tables import User

router = APIRouter(prefix='/user')


@router.post("/")
async def create_user(data: UserCreateModel, session: AsyncSession = Depends(create_session)):
    """Creates a new user and return new user"""
    result = await session.execute(select(User).where(User.username == data.username))
    user: User = result.scalar_one_or_none()

    if user:
        raise HTTPException(status_code=400, detail="User already exist")

    new_user = User(
        username=data.username,
        email=data.email,
        hashed_password=data.password
    )
    session.add(new_user)
    await session.commit()

    return new_user


@router.get("/{username}")
async def get_user(username: str, session: AsyncSession = Depends(create_session)):
    """Return founded user by username"""
    result = await session.execute(select(User).where(User.username == username))
    user: User = result.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user


