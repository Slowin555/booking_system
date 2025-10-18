from fastapi import APIRouter, Depends

from .deps import get_current_user


router = APIRouter(prefix="/auth", tags=["auth"])


@router.get("/me")
def me(user = Depends(get_current_user)):
    return {"id": str(user.id), "email": user.email, "role": user.role}


