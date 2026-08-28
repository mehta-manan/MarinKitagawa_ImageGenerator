from pydantic import BaseModel, Field, EmailStr
from typing import Annotated

UserId = Annotated[
    str,
    Field(
        min_length=5,
        max_length=15,
        description="Public user ID, user-created"
    )
]
Name = Annotated[str, Field(min_length=3, max_length=15)]
Email = Annotated[EmailStr, Field(max_length=60)]
Password = Annotated[str, Field(min_length=8)]
Age = Annotated[int, Field(ge=10, le=150)]

class UserBase(BaseModel):
    first_name: Name
    last_name: Name | None = None
    email: Email
    age: Age | None = None

class GetUserResponseBody(UserBase):
    id: UserId
    
class PostSignupUserRequestBody(UserBase):
    id: UserId
    password: Password

class PostSignupUserResponseBody(BaseModel):
    jwt: str
    
class PostSigninUserRequestBody(BaseModel):
    id: UserId | None = None
    email: Email | None = None
    password: Password
    
class PostSigninUserResponseBody(BaseModel):
    jwt: str