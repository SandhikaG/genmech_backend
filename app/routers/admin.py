from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.core.security import admin_required, get_db
from app.models.user import User

router = APIRouter(
    prefix="/admin",
    tags=["Admin"]
)


@router.get("/dashboard")
def get_admin_dashboard(
    db: Session = Depends(get_db),
    current_user: User = Depends(admin_required)
):
    total_users = db.query(func.count(User.id)).scalar()
    total_engineers = db.query(func.count(User.id))\
        .filter(User.role == "engineer")\
        .scalar()

    total_admins = db.query(func.count(User.id))\
        .filter(User.role == "admin")\
        .scalar()

    return {
        "message": f"Welcome {current_user.full_name}",
        "total_users": total_users,
        "total_engineers": total_engineers,
        "total_admins": total_admins
    }


@router.get("/engineers")
def list_engineers(
    db: Session = Depends(get_db),
    current_user: User = Depends(admin_required)
):
    engineers = db.query(User)\
        .filter(User.role == "engineer")\
        .all()

    return engineers