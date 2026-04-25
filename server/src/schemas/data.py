from dataclasses import dataclass
from datetime import datetime


@dataclass
class JWT_Payload:
    user_id: int
    first_name: str
    last_name: str
    email: str
    university: str
    state: str
    created_at: datetime
    last_login: datetime
    updated_at: datetime
