from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta
from app.db.database import get_session
from app.models.user import User, UserRole, UserCreate, UserResponse, UserLogin, Token
from app.core.config import settings
from app.api.dependencies import get_current_user,get_current_pm,get_session

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

@router.post("/register", response_model=UserResponse)
def register_user(user: UserCreate, session: Session = Depends(get_session)):
    # Check if user already exists
    statement = select(User).where(User.email == user.email)
    db_user = session.exec(statement).first()
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Check if username already exists
    statement = select(User).where(User.username == user.username)
    db_user = session.exec(statement).first()
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already taken"
        )
    
    # Check if this is the first user (make them PM)
    statement = select(User)
    users = session.exec(statement).all()
    user_count = len(users)
    #check if PM already exists 
    pm_exists = session.query(User).filter(User.role == UserRole.PM).first()
    user_count = session.query(User).count()
    
    # If no users exist, assign PM role automatically
    if user_count == 0:
        role = UserRole.PM
    else:
    # If user is trying to register as PM
        if user.role == UserRole.PM:
            if pm_exists:
                raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="A PM already exists. Please select either Developer or Designer role."
            )
            else:
                role = UserRole.PM
        else:
            role = user.role  # Allow Developer or Designer

# Create user
    hashed_password = get_password_hash(user.password)
    db_user = User(
    email=user.email,
    username=user.username,
    password_hash=hashed_password,
    role=role
    )
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user

@router.post("/login", response_model=Token)
def login(user_credentials: UserLogin, session: Session = Depends(get_session)):
    statement = select(User).where(User.email == user_credentials.email)
    user = session.exec(statement).first()
    
    if not user or not verify_password(user_credentials.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", response_model=UserResponse)
def get_current_user_info(current_user: User = Depends(get_current_user)):
    return current_user

@router.get("/users", response_model=list[UserResponse])
def get_all_users(
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_pm)
):
    """Get all users - PM only"""
    statement = select(User).where(User.is_active == True)
    users = session.exec(statement).all()
    return users