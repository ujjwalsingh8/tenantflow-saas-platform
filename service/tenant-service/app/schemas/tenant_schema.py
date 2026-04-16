from pydantic import BaseModel

class TenantCreate(BaseModel):
    company_name: str
    domain: str | None = None


class TenantResponse(BaseModel):
    id: str
    company_name: str
    domain: str | None

    class Config:
        from_attributes = True
