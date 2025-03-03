from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional
import bcrypt
from bson import ObjectId
import datetime

class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate
    
    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError('Invalid ObjectId')
        return ObjectId(v)
    
    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")

class UserModel(BaseModel):
    id: Optional[PyObjectId] = Field(alias='_id', default=None)
    name: str
    email: EmailStr
    password: str
    created_at: datetime.datetime = Field(default_factory=datetime.datetime.now)
    updated_at: datetime.datetime = Field(default_factory=datetime.datetime.now)
    
    class Config:
        arbitrary_types_allowed = True
        json_encoders = {
            ObjectId: str
        }
        schema_extra = {
            "example": {
                "name": "John Doe",
                "email": "john.doe@example.com",
                "password": "securePassword123"
            }
        }
    
    @validator('password')
    def hash_password(cls, v):
        return bcrypt.hashpw(v.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

class UserResponseModel(BaseModel):
    id: PyObjectId = Field(alias='_id')
    name: str
    email: EmailStr
    created_at: datetime.datetime
    updated_at: datetime.datetime
    
    class Config:
        arbitrary_types_allowed = True
        json_encoders = {
            ObjectId: str
        }

class UserUpdateModel(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    updated_at: datetime.datetime = Field(default_factory=datetime.datetime.now)
    
    class Config:
        arbitrary_types_allowed = True
        json_encoders = {
            ObjectId: str
        }
        schema_extra = {
            "example": {
                "name": "John Updated",
                "email": "john.updated@example.com",
                "password": "newSecurePassword456"
            }
        }
    
    @validator('password')
    def hash_password(cls, v):
        if v:
            return bcrypt.hashpw(v.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        return v