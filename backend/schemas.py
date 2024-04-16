from typing import  Optional, Generic, TypeVar
from pydantic import BaseModel
from pydantic.generics import GenericModel
from datetime import date

T = TypeVar('T')

class EmployeeBase(BaseModel):
    first_name: str
    last_name: str
    email: str
    employee_type: int
    benefits: Optional[str]=None
    leaves: Optional[int]=None
    project: Optional[str]=None
    contract_end: Optional[date]=None

    class Config:
        orm_mode = True

class EmployeeTypeBase(BaseModel):
    description: Optional[str]=None

    class Config:
        orm_mode = True

class Response(GenericModel,Generic[T]):
    code: Optional[str]=None
    status: Optional[str]=None
    message: Optional[str]=None 
    result: Optional[dict]=None

class UserBase(BaseModel):
    username: str
    password: str
    is_superuser: bool

class ShowUserBase(BaseModel):
    id: int
    username: str
    is_active: bool

class Token(BaseModel):
    access_token: str
    token_type: str
