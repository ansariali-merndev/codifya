from pydantic import BaseModel, EmailStr

class RegisterSchema(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str
    password: str
    university: str
    state: str
