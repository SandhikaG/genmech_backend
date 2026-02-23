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
def admin_dashboard(
    current_user: User = Depends(admin_required),
    db: Session = Depends(get_db)
):
    engineers = db.query(User).filter(User.role == "engineer").all()

    return {
        "message": f"Welcome {current_user.full_name}",
        "total_users": db.query(User).count(),
        "total_engineers": len(engineers),
        "total_admins": db.query(User).filter(User.role == "admin").count(),
        "engineers": [
            {
                "id": e.id,
                "name": e.full_name,
                "email": e.email,
                "photo": "https://i.pravatar.cc/150?img=3"  # temp image
            }
            for e in engineers
        ]
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
