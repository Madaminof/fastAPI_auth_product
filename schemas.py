from pydantic import BaseModel
from typing import Optional

class SignUp(BaseModel):
    id: Optional[int] = None
    username: str
    email: str
    password: str
    is_active: bool
    is_staff: bool

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "username": "john_doe",
                "email": "john.doe@example.com",
                "password": "secret",
                "is_active": True,
                "is_staff": False
            }
        }

class ProductCreate(BaseModel):
    name: str
    price: int

    class Config:
        from_attributes = True

class Product(BaseModel):
    id: int
    name: str
    price: int

    class Config:
        from_attributes = True
