from pydantic import BaseModel, EmailStr

class RegisterSchema(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str
    password: str
    university: str
    state: str


class VerifyOtpSchema(BaseModel):
    email: EmailStr
    otp: str


class ResendOtpSchema(BaseModel):
    email: EmailStr


class LoginSchema(BaseModel):
    email: EmailStr
    password: str


class ChangedPasswordSchema(BaseModel):
    old_password: str
    new_password: str


class ResetPasswordSchema(BaseModel):
    token: str
    new_password: str
