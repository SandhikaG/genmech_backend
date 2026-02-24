from fastapi import APIRouter, Depends,HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.core.security import admin_required, get_db
from app.models.user import User
from app.models.service_assignment import ServiceAssignment
from app.db.database import get_db
from app.core.security import get_current_user # or wherever yours is
from app.schemas.user import AssignServiceSchema
from app.models.company import Company

router = APIRouter()

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

@router.post("/assign-service")
def assign_service(
    data: AssignServiceSchema,
    current_user: User = Depends(admin_required),
    db: Session = Depends(get_db)
):
    new_assignment = ServiceAssignment(
    engineer_user_id=data.engineer_user_id,
    company_id=data.company_id,
    service_name=data.service_name
)

    db.add(new_assignment)
    db.commit()

    return {"message": "Service assigned successfully"}

@router.get("/engineers")
def list_engineers(
    db: Session = Depends(get_db),
    current_user: User = Depends(admin_required)
):
    engineers = db.query(User)\
        .filter(User.role == "engineer")\
        .all()

    return engineers

@router.get("/services")
def get_all_services(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not authorized")

    services = db.query(ServiceAssignment).all()

    result = []

    for service in services:
        user = db.query(User).filter(User.id == service.engineer_user_id).first()
        company = db.query(Company).filter(Company.id == service.company_id).first()

        result.append({
            "service_id": service.id,
            "engineer_name": user.full_name if user else "Unknown",
            "engineer_email": user.email if user else "Unknown",
            "company_name": company.company_name if company else "Unknown",
            "service_name": service.service_name,
            "status": service.status
        })

    return result


@router.get("/companies")
def get_companies(
    current_user: User = Depends(admin_required),
    db: Session = Depends(get_db)
):
    companies = db.query(Company).all()

    return [
        {
            "id": c.id,
            "company_name": c.company_name
        }
        for c in companies
    ]