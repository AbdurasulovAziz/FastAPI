from fastapi import FastAPI
from app.account.routes import router as account_router
from app.library.routes import router as app_router
from app.auth.routes import router as auth_router
app = FastAPI()

app.include_router(account_router)
app.include_router(app_router)
app.include_router(auth_router)

