from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
from schemas import SignUp
from models import User
from werkzeug.security import generate_password_hash, check_password_hash

router = APIRouter(
    prefix="/auth"
)


@router.get('/')
async def auth():
    return {'message': 'Authenticated'}


@router.get('/get_name')
async def get_name():
    return {'message': 'Samandar'}


@router.post('/signup')
async def signup(user: SignUp, db: Session = Depends(SessionLocal)):
    db_email = db.query(User).filter(User.email == user.email).first()
    if db_email:
        raise HTTPException(status_code=400, detail="Email already exists")

    db_username = db.query(User).filter(User.username == user.username).first()
    if db_username:
        raise HTTPException(status_code=400, detail="Username already exists")

    hashed_password = generate_password_hash(user.password)
    new_user = User(
        username=user.username,
        email=user.email,
        password=hashed_password,
        is_active=user.is_active,
        is_staff=user.is_staff
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {'message': 'User created successfully', 'new_user': new_user}
