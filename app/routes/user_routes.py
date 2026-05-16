from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import (
    OAuth2PasswordBearer,
    OAuth2PasswordRequestForm
)

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.database import SessionLocal
from app.models import User

from app.utils.redis_blacklist import (
    add_to_blacklist,
    is_blacklisted
)

from app.schemas import (
    UserCreate,
    UserResponse,
    TokenResponse
)

from app.utils.security import (
    hash_password,
    verify_password,
    create_access_token,
    create_refresh_token,
    verify_access_token,
    verify_refresh_token
)

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="login"
)


# =========================
# DATABASE
# =========================

async def get_db():

    async with SessionLocal() as db:
        yield db


# =========================
# REGISTER
# =========================

@router.post(
    "/register",
    response_model=UserResponse
)
async def register(
    user: UserCreate,
    db: AsyncSession = Depends(get_db)
):

    result = await db.execute(
        select(User).where(
            User.email == user.email
        )
    )

    existing_user = result.scalar_one_or_none()

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )

    hashed_password = hash_password(
        user.password
    )

    new_user = User(
        username=user.username,
        email=user.email,
        password=hashed_password
    )

    db.add(new_user)

    await db.commit()

    await db.refresh(new_user)

    return new_user


# =========================
# LOGIN
# =========================

@router.post(
    "/login",
    response_model=TokenResponse
)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db)
):

    result = await db.execute(
        select(User).where(
            User.email == form_data.username
        )
    )

    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid email"
        )

    if not verify_password(
        form_data.password,
        user.password
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid password"
        )

    access_token = create_access_token(
        data={"sub": user.email}
    )

    refresh_token = create_refresh_token(
        data={"sub": user.email}
    )

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }


# =========================
# PROTECTED ROUTE
# =========================

@router.get("/protected")
async def protected_route(
    token: str = Depends(oauth2_scheme)
):

    if await is_blacklisted(token):
        raise HTTPException(
            status_code=401,
            detail="Token has been revoked"
        )

    payload = verify_access_token(token)

    if not payload:
        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )

    return {
        "message": "Protected route accessed",
        "payload": payload
    }


# =========================
# CURRENT USER (/me)
# =========================

@router.get("/me")
async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db)
):

    if await is_blacklisted(token):
        raise HTTPException(
            status_code=401,
            detail="Token has been revoked"
        )

    payload = verify_access_token(token)

    if not payload:
        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )

    email = payload.get("sub")

    result = await db.execute(
        select(User).where(
            User.email == email
        )
    )

    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return {
        "id": user.id,
        "username": user.username,
        "email": user.email
    }


# =========================
# REFRESH TOKEN
# =========================

@router.post("/refresh")
async def refresh_token(
    refresh_token: str
):

    payload = verify_refresh_token(
        refresh_token
    )

    if not payload:
        raise HTTPException(
            status_code=401,
            detail="Invalid refresh token"
        )

    email = payload.get("sub")

    new_access_token = create_access_token(
        data={"sub": email}
    )

    return {
        "access_token": new_access_token,
        "token_type": "bearer"
    }


# =========================
# LOGOUT
# =========================

@router.post("/logout")
async def logout(
    token: str = Depends(oauth2_scheme)
):

    await add_to_blacklist(token)

    return {
        "detail": "Logout successful"
    }