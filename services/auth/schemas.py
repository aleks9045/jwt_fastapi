from pydantic import BaseModel, EmailStr, Field


class UserCreateSchema(BaseModel):
    # email: EmailStr = Field(title="user's email")
    name: str = Field(title="user's name")
    password: str = Field(title="user's password")


class UserLoginSchema(BaseModel):
    # email: EmailStr = Field(title="user's email")
    name: str = Field(title="user's name")
    password: str = Field(title="user's password")
