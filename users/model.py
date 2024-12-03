from pydantic import BaseModel, EmailStr, Field, SecretStr
from typing import Optional

class UserCreate(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    password: SecretStr
    phone_number: str
    dept_id: Optional[str] = Field(None, description="Department ID")
    location_id: Optional[str] = Field(None, description="Location ID")
    user_role: str

class UserView(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    phone_number: str
    dept_name: Optional[str] = Field(None, description="Department Name")
    location_name: Optional[str] = Field(None, description="Location Name")
    user_role: str
