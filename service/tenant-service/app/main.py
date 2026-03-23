from fastapi import FastAPI
from app.routers.tenant_router import router


app = FastAPI()

app.include_router(router)
