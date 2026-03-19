from fastapi import FastAPI, HTTPException, File, UploadFile, Form, Depends
from app.schemas import PostCreate, PostResponse

# db imports 
from app.db import Post, create_db_and_tables, get_async_session, User
from app.images import imagekit
import shutil
import os 
import tempfile
import uuid

# to create db automatically if not yet created 
from sqlalchemy.ext.asyncio import AsyncSession
from contextlib import asynccontextmanager
from sqlalchemy import select

# user db imports
from app.users import auth_backend, current_active_user, fastapi_Users

# schemas
from app.schemas import UserCreate, UserRead, UserUpdate

@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_db_and_tables()
    yield


app = FastAPI(lifespan=lifespan)

# including all endpoints from fastapi users 
app.include_router(fastapi_Users.get_auth_router(auth_backend), prefix="/auth/jwt", tags=["auth"])
app.include_router(fastapi_Users.get_register_router(UserRead, UserCreate), prefix="/auth", tags=["auth"])
app.include_router(fastapi_Users.get_reset_password_router(), prefix="/auth", tags=["auth"])
app.include_router(fastapi_Users.get_verify_router(UserRead), prefix="/auth", tags=["auth"])
app.include_router(fastapi_Users.get_users_router(UserRead, UserUpdate), prefix="/users", tags=["users"])


# endpoint to make new post
@app.post("/upload")
async def upload_file(
    file: UploadFile = File(...),
    caption: str = Form(""),
    # user must be authenticated to access endpoint
    user: User = Depends(current_active_user),
    session: AsyncSession = Depends(get_async_session)
):
    
    temp_file_path = None

    try: 
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(f"{file.filename}")[1]) as temp_file:
            temp_file_path = temp_file.name
            shutil.copyfileobj(file.file, temp_file)

            with open(temp_file_path, "rb") as file_for_upload:
                upload_result = imagekit.files.upload(
                    file=file_for_upload, 
                    file_name=f"{file.filename}",
                    use_unique_file_name=False,
                    tags=["backend-upload"],
                )

                if upload_result and hasattr(upload_result, 'url'):
                    
                    '''
                    how to create a new object in db
                    ~ Create object
                    ~session.add(object)
                    ~await sesssion.commit()
                    ~await session.refresh(object)

                    refreshing populates the object with missing data fields like id and created_at in this context
                    '''
                    post = Post(
                        user_id = user.id,
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
    session: AsyncSession = Depends(get_async_session),
    # User must be authenticated to acceess endpoint
    user: User = Depends(current_active_user)
):
    # executing a query for all posts
    result = await session.execute(select(Post).order_by(Post.created_at.desc()))
    posts = [row[0] for row in result.all()]

    result = await session.execute(select(User))
    users = [row[0] for row in result.all()]
    user_dict = {u.id: u.email for u in users}

    posts_data = []
    for post in posts:
        posts_data.append(
            {
                "id": str(post.id),
                "user_id": str(post.user_id),
                "caption": post.caption,
                "url": post.url,
                "file_type": post.file_type,
                "file_name": post.file_name,
                "created_at": post.created_at.isoformat(),
                "is_owner": post.user_id == user.id,
                "email": user_dict.get(post.user_id, "User not Found😢")
            }
        )

    return {'posts': posts_data}


# ednpoint to delete post
@app.delete('/posts/{post_id}')
async def delete_post(post_id: str, session: AsyncSession = Depends(get_async_session), user: User = Depends(current_active_user)):
    try: 
        post_uuid = uuid.UUID(post_id)

        # query selector
        result = await session.execute(select(Post).where(Post.id == post_uuid))

        # returns the exact result
        post = result.scalars().first()

        if not post:
            raise HTTPException(status_code=404, detail="Post not found :/")

        if str(post.user_id) != str(user.id):
            raise HTTPException(status_code=403, detail="You are not authorized to delete this!😡")
        
        # to delete post and reflect change in database
        await session.delete(post)
        await session.commit()
        return {"success ": True, "message":"Post is permanently expunged!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))