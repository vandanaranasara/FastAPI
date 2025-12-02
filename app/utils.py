from passlib.context import CryptContext
from fastapi import HTTPException

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(plain, hashed):
    return pwd_context.verify(plain, hashed)

def admin_required(user):
    if user.role != "admin":
        raise HTTPException(403, "Admin only access")

