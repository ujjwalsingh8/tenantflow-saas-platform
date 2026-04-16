from fastapi import FastAPI
from app.api.auth_router import router


app = FastAPI()

app.include_router(router)