from src.utils import success_res, error_res, hash_password, get_otp
from src.schemas import RegisterSchema
from src.models import User
from sqlalchemy.orm import Session
from src.configs import send_mail
from sqlalchemy import select
from datetime import datetime, timezone, timedelta


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
        message="User registered successfully. Please verify your email using OTP."
    )
