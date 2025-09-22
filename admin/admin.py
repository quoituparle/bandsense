from fastapi import  status, HTTPException, APIRouter, Depends
from sqlmodel import Session
from pydantic import BaseModel, Field

from ..database import get_db
from ..auth.views import get_current_user
from ..models import User, Topic

router = APIRouter(prefix="/admin", tags=["Admin App"])

