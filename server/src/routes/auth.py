from fastapi import APIRouter, Depends
from src.controllers import register_func, auth_root_func
from src.schemas import RegisterSchema
from sqlalchemy.orm import Session
from src.configs import get_db

auth_router = APIRouter(prefix="/auth")


@auth_router.get("")
def auth_root():
    return auth_root_func()


@auth_router.post("/register")
async def register_user(body: RegisterSchema, db: Session = Depends(get_db)):
    return await register_func(body, db)


@auth_router.post("/verify-otp")
def verify_otp():
    pass


@auth_router.post("/resend-otp")
def resend_otp():
    pass


@auth_router.post("/login")
def login_user():
    pass


@auth_router.get("/me")
def get_current_user():
    pass


@auth_router.post("/change-password")
def change_password():
    pass


@auth_router.post("/forgot-password")
def forgot_password():
    pass


@auth_router.post("/reset-password")
def reset_password():
    pass
