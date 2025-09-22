import datetime
import uuid

from pydantic import EmailStr
from sqlmodel import Field, SQLModel
from sqladmin import ModelView

class UserBase(SQLModel):
    email: EmailStr = Field(unique=True, index=True, max_length=255)
    is_active: bool = True
    is_superuser: bool = False
    full_name: str | None = Field(default=None, max_length=255)
    
class UserRegister(SQLModel):
    email: EmailStr = Field(max_length=255)
    password: str = Field(min_length=8, max_length=40)
    full_name: str | None = Field(default=None, max_length=255)

class UserLogin(SQLModel):
    email: EmailStr = Field(max_length=255)
    password: str = Field(min_length=8, max_length=40)

class User(UserBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid5, primary_key=True)
    hashed_password: str
    is_verified: bool = Field(default=False)
    verification_code: str | None = Field(default=None, index=True)
    code_expires_at: datetime.datetime | None = Field(default=None)
    api_key: str | None = Field(default=None)
    language: str

class Topic(SQLModel):
    essay_topic: str
    essay_topic_id: uuid.UUID = Field(default_factory=uuid.uuid5)
    published_essay: str | None
    published_score: float | None
    published_date: datetime.datetime | None = Field(default=None)

class UserAdmin(ModelView, model=User):
    column_list = [User.id, User.full_name, User.email]
    can_create = True
    can_edit = True
    can_delete = True
    can_view_details = True
    name = "User"
    name_plural = "Users"
    icon = "fa-solid fa-user"
    identity = "user"