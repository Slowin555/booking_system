from __future__ import annotations

from pydantic import BaseModel, EmailStr, Field
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import User, RoleEnum
from app.db import get_session
from .security import hash_password
from .ratelimit import limiter


router = APIRouter(prefix="/auth", tags=["auth"])


class RegisterBody(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)


@router.post("/register", status_code=status.HTTP_201_CREATED)
@limiter.limit("5/minute")
def register(body: RegisterBody, session: Session = Depends(get_session)):
    existing = session.execute(select(User).where(User.email.ilike(body.email))).scalar_one_or_none()
    if existing:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already in use")
    user = User(email=body.email, password_hash=hash_password(body.password), role=RoleEnum.USER)
    session.add(user)
    session.commit()
    return {"id": str(user.id), "email": user.email, "role": user.role}


