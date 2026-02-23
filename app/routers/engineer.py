from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.models.engineer import Engineer
from app.models.user import User
from app.core.security import get_current_user

router = APIRouter(prefix="/engineer", tags=["Engineer"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/admin/engineer/{engineer_id}")
def get_engineer_details(engineer_id: str, db: Session = Depends(get_db)):
    engineer = db.query(Engineer).filter(Engineer.id == engineer_id).first()

    if not engineer:
        raise HTTPException(status_code=404, detail="Engineer not found")

    user = db.query(User).filter(User.id == engineer.user_id).first()

    return {
        "full_name": user.full_name,
        "email": user.email,
        "phone": user.phone,
        "address": engineer.address,
        "portfolio_image": engineer.portfolio_image,
        "services_completed": engineer.services_completed
    }
# ✅ STEP 4 — GET ENGINEER PROFILE
@router.get("/profile")
def get_engineer_profile(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if current_user.role != "engineer":
        raise HTTPException(status_code=403, detail="Not authorized")

    engineer = db.query(Engineer).filter(
        Engineer.user_id == current_user.id
    ).first()

    return {
        "email": current_user.email,
        "full_name": current_user.full_name,
        "phone": current_user.phone,
        "address": engineer.address if engineer else None,
        "portfolio_image": engineer.portfolio_image if engineer else None,
        "services_completed": engineer.services_completed if engineer else 0,
    }


# ✅ STEP 5 — UPDATE ENGINEER PROFILE
@router.put("/profile")
def update_engineer_profile(
    phone: str,
    address: str,
    portfolio_image: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.role != "engineer":
        raise HTTPException(status_code=403, detail="Not authorized")

    engineer = db.query(Engineer).filter(
        Engineer.user_id == current_user.id
    ).first()

    if not engineer:
        engineer = Engineer(user_id=current_user.id)
        db.add(engineer)

    # ✅ Update user phone
    user = db.query(User).filter(User.id == current_user.id).first()
    user.phone = phone

    # ✅ Update engineer fields
    engineer.address = address
    engineer.portfolio_image = portfolio_image

    db.commit()
    db.refresh(user)
    db.refresh(engineer)

    return {"message": "Profile updated successfully"}