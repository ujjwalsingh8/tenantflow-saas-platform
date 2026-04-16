from app.database import Base
from sqlalchemy import Column, Integer, String


class AuthUser(Base):
    __tablename__ = 'auth_users'

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String)
    password_hash = Column(String)
    tenant_id = Column(String)
    