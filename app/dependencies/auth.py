from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.database import SessionLocal
from app.models import User
from app.utils.security import verify_access_token
from app.utils.redis_blacklist import is_blacklisted

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="login"
)


async def get_db():

    async with SessionLocal() as session:
        yield session


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db)
):

    if await is_blacklisted(token):
        raise HTTPException(
            status_code=401,
            detail="Token revoked"
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

    user = result.scalars().first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return user