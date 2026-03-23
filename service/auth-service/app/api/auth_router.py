from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.auth_schema import SignupRequest, LoginRequest, TokenResponse
from app.services.auth_service import signup_user, login_user
from app.utils.hash import get_current_user


router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/signup")
def signup(
    request: SignupRequest,
    db: Session = Depends(get_db),
    tenant_id: str = Header(...) 
):
    user = signup_user(db, request.email, request.password, tenant_id)
    return {"message": "User created"}


@router.post("/login", response_model=TokenResponse)
def login(request: LoginRequest, db: Session = Depends(get_db)):
    try:
        return login_user(db, request.email, request.password)
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))

@router.get("/me")
def get_me(current_user=Depends(get_current_user)):
    return {
        "user_id": current_user["user_id"],
        "tenant_id": current_user["tenant_id"]
    }

