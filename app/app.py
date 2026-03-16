from fastapi import FastAPI, HTTPException
from app.schemas import PostCreate, PostResponse

# db imports 
from app.db import Post, create_db_and_tables, get_async_session

# to create db automatically if not yet created 
from sqlalchemy.ext.asyncio import AsyncSession
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_db_and_tables()
    yield


app = FastAPI(lifespan=lifespan)
