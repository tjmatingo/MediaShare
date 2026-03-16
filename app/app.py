from fastapi import FastAPI, HTTPException, File, UploadFile, Form, Depends
from app.schemas import PostCreate, PostResponse

# db imports 
from app.db import Post, create_db_and_tables, get_async_session

# to create db automatically if not yet created 
from sqlalchemy.ext.asyncio import AsyncSession
from contextlib import asynccontextmanager
from sqlalchemy import select

@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_db_and_tables()
    yield


app = FastAPI(lifespan=lifespan)

# endpoint to make new post
@app.post("/upload")
async def upload_file(
    file: UploadFile = File(...),
    caption: str = Form(""),
    session: AsyncSession = Depends(get_async_session)
):
    
    '''
    how to create a new object in db
    ~ Create object
    ~session.add(object)
    ~await sesssion.commit()
    ~await session.refresh(object)

    refreshing populates the object with missing data fields like id and created_at in this context
    '''
    post = Post(
        caption=caption,
        url="dummy url",
        file_type="photo",
        file_name="dummy name"
    )

    session.add(post)
    await session.commit()
    await session.refresh(post)

    return post


# endpoint to see posts
@app.get('/feed')
async def get_feed(
    session: AsyncSession = Depends(get_async_session)
):
    # executing a query for all posts
    result  = await session.execute(select(Post).order_by(Post.created_at.desc()))
    posts = [row[0] for row in result.all()]


    posts_data = []
    for post in posts:
        posts_data.append(
            {
                "id": str(post.id),
                "caption": post.caption,
                "url": post.url,
                "file_type": post.file_type,
                'file_name': post.file_name,
                "created_at": post.created_at.isoformat(),
            }
        )

    return {'posts': posts_data}