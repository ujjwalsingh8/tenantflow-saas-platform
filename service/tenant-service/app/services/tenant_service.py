from sqlalchemy.orm import Session
from app.models.tenant_model import Tenant

def create_tenant(db: Session, company_name: str, domain: str = None):
    tenant = Tenant(
        company_name=company_name,
        domain=domain
    )

    db.add(tenant)
    db.commit()
    db.refresh(tenant)

    return tenant


def get_tenant(db: Session, tenant_id: str):
    return db.query(Tenant).filter(Tenant.id == tenant_id).first()
