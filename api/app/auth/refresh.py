from __future__ import annotations

from typing import Optional

from fastapi import APIRouter, Cookie, Depends, HTTPException, Response, status, Request

from .security import JWTSettings, create_access_token, decode_token
from .deps import get_jwt_settings
from .ratelimit import limiter


router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/refresh")
@limiter.limit("5/minute")
def refresh(
    request: Request,
    response: Response,
    settings: JWTSettings = Depends(get_jwt_settings),
    refresh_token: Optional[str] = Cookie(default=None, alias="refresh_token"),
):
    if not refresh_token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing refresh token")
    payload = decode_token(settings, refresh_token)
    if not payload or payload.get("type") != "refresh":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")
    subject = payload.get("sub")
    if not subject:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token payload")
    new_access = create_access_token(settings, subject)
    response.set_cookie("access_token", new_access, httponly=True, samesite="lax")
    return {"ok": True}


