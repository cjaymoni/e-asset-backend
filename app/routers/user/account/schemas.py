from routers.user.role.schemas import Role
from typing import Optional, List, Union
import routers.user.account.models as m
from pydantic import BaseModel, constr
from constants import EMAIL, PHONE
import datetime, enum

class Account(str, enum.Enum):
    users = 'users'
    administrators = 'administrators'

class EmailBase(BaseModel):
    email: constr(regex=EMAIL)
    
class PasswordBase(BaseModel):
    password: constr(min_length=8)

class UpdatePassword(PasswordBase):
    code: str
    password: constr(min_length=8)
    
class CreateAdmin(EmailBase):
    password: constr(min_length=8) = None
    
    class Meta:
        model = m.Administrator

class Admin(EmailBase):
    id: int
    push_id: str
    is_active: bool
    created: datetime.datetime
    updated: datetime.datetime
    
    class Config:
        orm_mode = True

class CreateUser(EmailBase):
    role_id:int
    last_name:str
    first_name:str
    middle_name:Optional[str]
    is_active:Optional[bool]
    phone: Optional[constr(regex=PHONE)]
    password: constr(min_length=8) = None
    
    class Meta:
        model = m.User

class UpdateUser(BaseModel):
    role_id:Optional[int]
    last_name:Optional[str]
    first_name:Optional[str]
    middle_name:Optional[str]
    is_active:Optional[bool]
    phone: Optional[constr(regex=PHONE)]
    password: Optional[UpdatePassword]
    
    class Meta:
        model = m.User

class User(EmailBase):
    id: int 
    phone:str
    push_id: str
    last_name:str
    first_name:str
    is_active:bool
    role: Optional[Role]
    middle_name:Optional[str]
    created: datetime.datetime
    updated: datetime.datetime
    department_id: Optional[int]

    class Config:
        orm_mode = True

class UserOrAdminList(BaseModel):
    bk_size: int
    pg_size: int
    data: Union[List[User], List[Admin], list]

class UserSummary(BaseModel):
    id:int
    last_name: Optional[str]
    first_name: Optional[str]
    middle_name: Optional[str]
    email: constr(regex=EMAIL)
    department_id: Optional[int]
    phone: Optional[constr(regex=PHONE)]
   
    class Config:
        orm_mode = True