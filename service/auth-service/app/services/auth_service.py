from sqlalchemy.orm import Session
from app.models.user_model import AuthUser
from app.utils.hash import hash_password, verify_password
from app.utils.jwt import create_access_token, create_refresh_token


def signup_user(db: Session, email: str, password: str, tenant_id: str):
    existing_user = db.query(AuthUser).filter(AuthUser.email == email).first()
    
    if existing_user:
        raise Exception("User already exists")

    user = AuthUser(
        email=email,
        password_hash=hash_password(password),
        tenant_id=tenant_id
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user


def login_user(db: Session, email: str, password: str):
    user = db.query(AuthUser).filter(AuthUser.email == email).first()

    if not user:
        raise Exception("Invalid credentials")

    if not verify_password(password, user.password_hash):
        raise Exception("Invalid credentials")

    access_token = create_access_token({
        "user_id": user.id,
        "tenant_id": user.tenant_id
    })

    refresh_token = create_refresh_token({
        "user_id": user.id,
        "tenant_id": user.tenant_id
    })

    return {
        "access_token": access_token,
        "refresh_token": refresh_token
    }
