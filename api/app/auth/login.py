from __future__ import annotations

from pydantic import BaseModel, EmailStr
from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import User
from app.db import get_session
from .security import JWTSettings, create_access_token, create_refresh_token, verify_password
from .deps import get_jwt_settings
from .ratelimit import limiter


router = APIRouter(prefix="/auth", tags=["auth"])


class LoginBody(BaseModel):
    email: EmailStr
    password: str


@router.post("/login")
@limiter.limit("5/minute")
def login(
    body: LoginBody,
    response: Response,
    session: Session = Depends(get_session),
    settings: JWTSettings = Depends(get_jwt_settings),
):
    user = session.execute(select(User).where(User.email.ilike(body.email))).scalar_one_or_none()
    if not user or not verify_password(body.password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    access = create_access_token(settings, str(user.id))
    refresh = create_refresh_token(settings, str(user.id))
    # HttpOnly cookies
    response.set_cookie("access_token", access, httponly=True, samesite="lax")
    response.set_cookie("refresh_token", refresh, httponly=True, samesite="lax")
    return {"ok": True}


