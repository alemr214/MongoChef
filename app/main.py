from contextlib import asynccontextmanager
from fastapi import FastAPI
from database import init
from routers import users_routers
from typing import AsyncGenerator, Any


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, Any]:
    """
    Lifespan event handler for the FastAPI application to make a connection with MongoDB using Beanie ODM.

    Args:
        app (FastAPI): FastAPI application instance.
    """
    app.state.mongo_client = await init()
    yield
    await app.state.mongo_client.close()


# Instance with the initial settings
app = FastAPI(
    title="MongoChef API",
    description="API built with FastAPI and MongoDB for a Recipe Management System.",
    version="1.0.0",
    docs_url="/docs",
    lifespan=lifespan,  # Event handler for the lifespan of the app
)

app.include_router(users_routers.router, tags=["users"])
