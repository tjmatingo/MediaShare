from fastapi import FastAPI, HTTPException, File, UploadFile, Form, Depends
from app.schemas import PostCreate, PostResponse

# db imports 
from app.db import Post, create_db_and_tables, get_async_session
from app.images import imagekit
import shutil
import os 
import tempfile
import uuid



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
    
    temp_file_path = None

    try: 
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(f"{file.filename}")[1]) as temp_file:
            temp_file_path = temp_file.name
            shutil.copyfileobj(file.file, temp_file)

            upload_result = imagekit.files.upload(
                file=open(temp_file_path, "rb"), 
                file_name=f"{file.filename}",
                use_unique_file_name=False,
                tags=["backend-upload"],
            )

            if upload_result == 200:
                
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
                    url=upload_result.url,
                    file_type="video" if file.content_type.startswith("video/") else "image",
                    file_name=upload_result.name,
                )

                session.add(post)
                await session.commit()
                await session.refresh(post)

                return post

    except Exception as e: 
        raise HTTPException(status_code=500, detail=str(e))
    finally: 
        if temp_file_path and os.path.exists(temp_file_path):
            os.unlink(temp_file_path)
        file.file.close()
        
    


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
                "file_name": post.file_name,
                "created_at": post.created_at.isoformat(),
            }
        )

    return {'posts': posts_data}