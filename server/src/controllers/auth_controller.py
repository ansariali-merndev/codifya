from src.models import User
from sqlalchemy.orm import Session
from src.configs import send_mail, send_foget_password_mail
from sqlalchemy import select
from datetime import datetime, timezone, timedelta
from env import ENV
from fastapi import Request
from src.utils import (
    success_res,
    error_res,
    hash_password,
    get_otp,
    check_password,
    create_token,
    verify_token,
    create_forget_password_token,
)
from src.schemas import (
    RegisterSchema,
    VerifyOtpSchema,
    JWT_Payload,
    ResendOtpSchema,
    LoginSchema,
    ChangedPasswordSchema,
    ResetPasswordSchema,
)


def auth_root_func():
    return success_res("Welcome to the Auth service.")


async def register_func(body: RegisterSchema, db: Session):
    stmt = select(User).where(User.email == body.email)
    existing_user = db.execute(stmt).scalar_one_or_none()

    otp = get_otp()
    otp_expiry = datetime.now(timezone.utc) + timedelta(minutes=10)

    if existing_user:
        if existing_user.is_verified:
            return error_res(
                "Email already registered. Please log in to continue.", 409
            )
        existing_user.first_name = body.first_name
        existing_user.last_name = body.last_name
        existing_user.password = hash_password(body.password)
        existing_user.otp = otp
        existing_user.otp_expiry = otp_expiry
        existing_user.university = body.university
        existing_user.state = body.state
        db.commit()
        db.refresh(existing_user)
        await send_mail(existing_user.email, otp)
        return success_res("OTP resent successfully. Please verify your email.")

    new_user = User(
        email=body.email,
        first_name=body.first_name,
        last_name=body.last_name,
        password=hash_password(body.password),
        otp=otp,
        otp_expiry=otp_expiry,
        university=body.university,
        state=body.state,
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    await send_mail(body.email, otp)

    return success_res(
        "User registered successfully. Please verify your email using OTP.", 201
    )


def verify_otp_func(body: VerifyOtpSchema, db: Session):
    stmt = select(User).where(User.email == body.email)
    user = db.execute(stmt).scalar_one_or_none()

    if not user:
        return error_res("Please register again to continue", 404)

    if user.is_verified:
        return error_res(
            "This email address has already been verified. Kindly log in to continue.",
            400,
        )

    if user.otp != body.otp:
        return error_res(
            "Invalid OTP. Please enter the correct verification code.", 400
        )

    if not user.otp_expiry or datetime.now(timezone.utc) > user.otp_expiry.replace(
        tzinfo=timezone.utc
    ):
        return error_res("OTP has expired. Please request a new one.", 400)

    user.is_verified = True
    user.otp = None
    user.otp_expiry = None
    db.commit()

    payload = JWT_Payload(
        user.id,
        user.first_name,
        user.last_name,
        user.email,
        user.university,
        user.state,
        user.created_at,
        user.last_login,
        user.updated_at,
    )

    token = create_token(payload)
    IS_PROD = ENV == "production"

    response = success_res("Email verified successfully.")
    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        max_age=7 * 24 * 60 * 60,
        samesite="none" if IS_PROD else "lax",
        secure=True if IS_PROD else False,
        path="/",
    )

    return response


async def resend_otp_func(body: ResendOtpSchema, db: Session):
    stmt = select(User).where(User.email == body.email)
    user = db.execute(stmt).scalar_one_or_none()

    if not user:
        return error_res("user not found", 404)

    if user.is_verified:
        return error_res(
            "This email is already registered. Please log in to continue.", 400
        )

    otp = get_otp()
    user.otp = otp
    user.otp_expiry = datetime.now(timezone.utc) + timedelta(minutes=10)
    db.commit()

    await send_mail(user.email, otp)
    return success_res("OTP resent successfully. Please check your email.")


def login_func(body: LoginSchema, db: Session):
    stmt = select(User).where(User.email == body.email)
    user = db.execute(stmt).scalar_one_or_none()

    if not user:
        return error_res("Incorrect email or password. Please try again.", 400)

    if not user.is_verified:
        return error_res("Incorrect email or password. Please try again.", 400)

    is_match = check_password(user.password, body.password)
    if not is_match:
        return error_res("Incorrect email or password. Please try again.", 400)

    user.last_login = datetime.now(timezone.utc)
    db.commit()
    db.refresh(user)

    payload = JWT_Payload(
        user.id,
        user.first_name,
        user.last_name,
        user.email,
        user.university,
        user.state,
        user.created_at,
        user.last_login,
        user.updated_at,
    )

    token = create_token(payload)
    IS_PROD = ENV == "production"

    response = success_res("Login successfully")
    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        max_age=7 * 24 * 60 * 60,
        samesite="none" if IS_PROD else "lax",
        secure=True if IS_PROD else False,
        path="/",
    )
    return response


def me_func(request: Request):
    token = request.cookies.get("access_token")
    if not token:
        return error_res("Unauthorized access. Please login again.", 401)

    payload = verify_token(token)
    if not payload:
        return error_res("Session expired or invalid token. Please login again.", 401)

    return success_res("User detailed fetched", data=payload)


def changed_password_func(body: ChangedPasswordSchema, request: Request, db: Session):
    token = request.cookies.get("access_token")
    if not token:
        return error_res("Failed to change password. Please try later", 400)

    payload = verify_token(token)
    if not payload:
        return error_res("Failed to change password. Please try later", 400)

    stmt = select(User).where(User.id == payload.get("user_id"))
    user = db.execute(stmt).scalar_one_or_none()

    if not user:
        return error_res("User not found", 400)

    if not check_password(user.password, body.old_password):
        return error_res(
            "The password you entered is incorrect. Please try again.", 400
        )

    user.password = hash_password(body.new_password)
    db.commit()
    return success_res("Your password has been changed successfully")


async def forget_password_func(body: ResendOtpSchema, db: Session):
    stmt = select(User).where(User.email == body.email)
    user = db.execute(stmt).scalar_one_or_none()

    if not user:
        return error_res(
            "We couldn't find an account with this email. Please register to continue.",
            400,
        )

    if not user.is_verified:
        return error_res(
            "We couldn't find an account with this email. Please register to continue.",
            400,
        )
    payload = {"user_id": user.id, "email": user.email, "type": "reset_password"}

    token = create_forget_password_token(payload)
    await send_foget_password_mail(user.email, token)

    return success_res("Please check your email. We've sent you a password reset link.")


def reset_password_func(body: ResetPasswordSchema, db: Session):
    payload = verify_token(body.token)

    if not payload:
        return error_res("Reset link is invalid or has expired. Please try again.", 400)

    if payload.get("type") != "reset_password":
        return error_res("Invalid token.", 400)

    stmt = select(User).where(User.id == payload.get("user_id"))
    user = db.execute(stmt).scalar_one_or_none()

    if not user:
        return error_res("User not found.", 404)

    user.password = hash_password(body.new_password)
    db.commit()

    return success_res(
        "Password reset successfully. You can now log in with your new password."
    )


def logout_func(request: Request):
    token = request.cookies.get("access_token")
    if not token:
        return error_res("You are not logged in.", 401)

    IS_PROD = ENV == "production"

    response = success_res("Logged out successfully.")
    response.delete_cookie(
        key="access_token",
        httponly=True,
        samesite="none" if IS_PROD else "lax",
        secure=True if IS_PROD else False,
        path="/",
    )
    return response
