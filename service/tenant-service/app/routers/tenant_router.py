from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.tenant_model import Tenant
from app.schemas.tenant_schema import TenantCreate, TenantResponse
from app.services.tenant_service import create_tenant, get_tenant

router = APIRouter(prefix="/tenant", tags=["Tenant"])


@router.post("/create", response_model=TenantResponse)
def create_tenant_api(request: TenantCreate, db: Session = Depends(get_db)):
    tenant = create_tenant(db, request.company_name, request.domain)
    return tenant

@router.get("/")
def list_tenants(db: Session = Depends(get_db)):
    return db.query(Tenant).all()

@router.get("/{tenant_id}")
def get_tenant_by_tenant_id(tenant_id: str, db: Session = Depends(get_db)):
    tenant = get_tenant(db, tenant_id)
    if not tenant:
        raise HTTPException(status_code=404, detail="Tenant not found")
    return tenant

@router.get("/validate/{tenant_id}")
def validate_tenant(tenant_id: str, db: Session = Depends(get_db)):
    tenant = db.query(Tenant).filter(
        Tenant.id == tenant_id,
        Tenant.is_active == True
    ).first()

    return {"valid": bool(tenant)}

@router.delete("/{tenant_id}")
def delete_tenant(tenant_id: str, db: Session = Depends(get_db)):
    tenant = get_tenant(db, tenant_id)
    if not tenant:
        raise HTTPException(status_code=404, detail="Tenant not found")

    tenant.is_active = False
    db.commit()
    return {"message": "Tenant deactivated successfully"}
