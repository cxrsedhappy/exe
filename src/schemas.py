from pydantic import BaseModel, EmailStr, Field


class UserCreateModel(BaseModel):
    """Validate data"""
    username: str = Field(example="username")
    email: EmailStr = Field(example="username@example.org")
    password: str = Field(example="password")


class UserData(UserCreateModel):
    """Validate database object"""
    id: int = Field(example="1")
    is_active: bool = Field(example="false")
