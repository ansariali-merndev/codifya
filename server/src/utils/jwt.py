import jwt
from datetime import datetime, timedelta, timezone
from env import SECRET_KEY
from src.schemas import JWT_Payload


def create_token(payload: JWT_Payload):
    data = {
        "user_id": payload.user_id,
        "email": payload.email,
        "first_name": payload.first_name,
        "last_name": payload.last_name,
        "university": payload.university,
        "state": payload.state,
        "created_at": payload.created_at.isoformat(),
        "last_login": payload.last_login.isoformat(),
        "updated_at": payload.updated_at.isoformat(),
    }

    expire = datetime.now(timezone.utc) + timedelta(days=7)
    data.update({"exp": expire})

    return jwt.encode(data, SECRET_KEY, algorithm="HS256")


def verify_token(token: str):
    try:
        return jwt.decode(token, SECRET_KEY, algorithms="HS256")
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None
