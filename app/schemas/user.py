from pydantic import BaseModel, Field
from typing import Optional



class UserBase(BaseModel):
    username: str=Field(min_length=4, max_length=20)
    email: str=Field(min_length=6, max_length=30)
    full_name: str=Field(min_length=5, max_length=20)
    password: str=Field(min_length=4, max_length=20)
    is_active: Optional[bool]=True
    is_staff: Optional[bool]=False


    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "username": "john_doe",
                "email": "john.doe@example.com",
                "full_name": "John Doe",
                "password": "secret",
                "is_staff": False,
                "is_active": True
            }
        }


class User(UserBase):
    id: int = Field(default=None, alias="userId")
