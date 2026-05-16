from fastapi import FastAPI
from contextlib import asynccontextmanager

import asyncio
import sys

if sys.platform.startswith("win"):
    asyncio.set_event_loop_policy(
        asyncio.WindowsSelectorEventLoopPolicy()
    )

from app.database import engine, Base
from app.routes.user_routes import router


@asynccontextmanager
async def lifespan(app: FastAPI):

    async with engine.begin() as conn:
        await conn.run_sync(
            Base.metadata.create_all
        )

    yield

    await engine.dispose()


app = FastAPI(
    title="Core Auth Backend",
    lifespan=lifespan
)

app.include_router(router)


@app.get("/")
async def home():

    return {
        "message": "Backend Running Successfully"
    }