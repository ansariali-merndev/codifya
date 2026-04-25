import jwt
from datetime import datetime, timedelta, timezone
from env import SECRET_KEY
from src.schemas import JWT_Payload
from typing import Dict

IST = timezone(timedelta(hours=5, minutes=30))


def to_ist(dt: datetime) -> str:
    if dt is None:
        return None
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(IST).isoformat()


def create_token(payload: JWT_Payload):
    data = {
        "user_id": payload.user_id,
        "email": payload.email,
        "first_name": payload.first_name,
        "last_name": payload.last_name,
        "university": payload.university,
        "state": payload.state,
        "created_at": to_ist(payload.created_at),
        "last_login": to_ist(payload.last_login),
        "updated_at": to_ist(payload.updated_at),
    }

    expire = datetime.now(IST) + timedelta(days=7)
    data.update({"exp": expire})

    return jwt.encode(data, SECRET_KEY, algorithm="HS256")


def create_forget_password_token(payload: Dict):
    expire = datetime.now(IST) + timedelta(minutes=5)
    payload.update({"exp": expire})
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")


def verify_token(token: str):
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None
