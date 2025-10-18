from __future__ import annotations

import os
from typing import Optional

from fastapi import Cookie, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import User
from .security import JWTSettings, decode_token
from ..db import get_session


def get_jwt_settings() -> JWTSettings:
    secret = os.getenv("JWT_SECRET", "dev-secret")
    return JWTSettings(secret_key=secret)


def get_current_user(
    session: Session = Depends(get_session),
    settings: JWTSettings = Depends(get_jwt_settings),
    access_token: Optional[str] = Cookie(default=None, alias="access_token"),
):
    if not access_token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    payload = decode_token(settings, access_token)
    if not payload or payload.get("type") != "access":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token payload")
    user = session.execute(select(User).where(User.id == user_id)).scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    return user


