from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from src.configs import get_db
from src.schemas import (
    RegisterSchema,
    VerifyOtpSchema,
    ResendOtpSchema,
    LoginSchema,
    ChangedPasswordSchema,
    ResetPasswordSchema,
)
from src.controllers import (
    register_func,
    auth_root_func,
    verify_otp_func,
    resend_otp_func,
    login_func,
    me_func,
    changed_password_func,
    forget_password_func,
    reset_password_func,
    logout_func,
)

auth_router = APIRouter(prefix="/auth")


@auth_router.get("")
def auth_root():
    return auth_root_func()


@auth_router.post("/register")
async def register_user(body: RegisterSchema, db: Session = Depends(get_db)):
    return await register_func(body, db)


@auth_router.post("/verify-otp")
def verify_otp(body: VerifyOtpSchema, db: Session = Depends(get_db)):
    return verify_otp_func(body, db)


@auth_router.post("/resend-otp")
async def resend_otp(body: ResendOtpSchema, db: Session = Depends(get_db)):
    return await resend_otp_func(body, db)


@auth_router.post("/login")
def login_user(body: LoginSchema, db: Session = Depends(get_db)):
    return login_func(body, db)


@auth_router.get("/me")
def get_current_user(request: Request):
    return me_func(request)


@auth_router.post("/change-password")
def change_password(
    body: ChangedPasswordSchema, request: Request, db: Session = Depends(get_db)
):
    return changed_password_func(body, request, db)


@auth_router.post("/forgot-password")
async def forgot_password(body: ResendOtpSchema, db: Session = Depends(get_db)):
    return await forget_password_func(body, db)


@auth_router.post("/reset-password")
def reset_password(body: ResetPasswordSchema, db: Session = Depends(get_db)):
    return reset_password_func(body, db)


@auth_router.post("/logout")
def logout(request: Request):
    return logout_func(request)
