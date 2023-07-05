from fastapi import FastAPI
from account.routes import router as account_router
from app.routes import router as app_router
from auth.routes import router as auth_router
app = FastAPI()

app.include_router(account_router)
app.include_router(app_router)
app.include_router(auth_router)

