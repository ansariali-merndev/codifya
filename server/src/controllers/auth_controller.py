from src.utils import success_res, error_res, hash_password, get_otp
from src.schemas import RegisterSchema, VerifyOtpSchema, JWT_Payload
from src.models import User
from sqlalchemy.orm import Session
from src.configs import send_mail
from sqlalchemy import select
from datetime import datetime, timezone, timedelta
from src.utils import create_token
from env import ENV


def auth_root_func():
    return success_res("Welcome to the Auth service.")


async def register_func(body: RegisterSchema, db: Session):
    stmt = select(User).where(User.email == body.email)
    existing_user = db.execute(stmt).scalar_one_or_none()

    otp = get_otp()
    otp_expiry = datetime.now(timezone.utc) + timedelta(minutes=10)

    if existing_user:
        if existing_user.is_verified:
            return error_res("Email already registered. Please log in to continue.")
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


def verify_otp_func(body: VerifyOtpSchema, db: Session, response):
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

    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        max_age=7 * 24 * 60 * 60,
        samesite="none" if IS_PROD else "lax",
        secure=True if IS_PROD else False,
        path="/",
    )

    return success_res("Email verified successfully.")
