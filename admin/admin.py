import os
from dotenv import load_dotenv

from fastapi import APIRouter
from sqlmodel import Session

from ..database import get_db
from ..auth.views import get_user

load_dotenv()
router = APIRouter(prefix="/admin", tags=["Admin App"])


def make_admin(db: Session, email: str):
    update_user = get_user(db, email)

    update_user.is_superuser = True

    try:
        db.add(update_user)
        db.commit()
        db.refresh(update_user)
    except Exception as e:
        db.rollback()
        print(f"Unable to update admin user, {e}")

make_admin(db=get_db, email=os.getenv('admin_email'))