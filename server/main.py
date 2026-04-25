from fastapi import FastAPI, Depends, HTTPException
from src.schemas import RegisterSchema
from sqlalchemy.orm import Session
from sqlalchemy import select
from src.models import User
from src.configs import get_db, Base, engine


Base.metadata.create_all(bind=engine)
app = FastAPI()

@app.get("/")
def root_route():
    return {
        "success":True,
        "message": "Welcome Codifya backend application"
    }
    
@app.get("/auth")
def auth_root():
    return {
        "success": False,
        "message": "Welcome to the auth API server"
    }
    
@app.post("/auth/register")
def register_func(body: RegisterSchema, db: Session = Depends(get_db)):
    stmt = select(User).where(User.email == body.email)
    
    result = db.execute(stmt)
    is_exist = result.scalar_one_or_none()

    if is_exist:
        raise HTTPException(
            status_code=409,
            detail="Email already exists"
        )

    new_user = User(
        email=body.email,
        first_name=body.first_name,
        last_name=body.last_name,
        password=body.password
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "success": True,
        "message": "User registered successfully"
    }