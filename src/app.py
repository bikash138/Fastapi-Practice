from fastapi import FastAPI, HTTPException
from src.database.db import get_db
from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.database.models import User, Post
from src.schemas import PostCreate, PostResponse, UserCreate, UserRespone

app = FastAPI()


@app.get("/")
def hello_world():
    return {
        "success": "true",
        "message": "Hello World" # This data will be automatically converted to JSON
    }

@app.post("/create-user")
async def create_user(user: UserCreate, db: AsyncSession = Depends(get_db)) -> UserRespone:
    try:
      new_user = User(username=user.username, email=user.email)
      db.add(new_user)
      await db.commit()
      return {
          "success": True,
          "message": "User created Successfully"
      }
    except Exception as e:
      raise HTTPException(status_code=500, detail=str(e))

@app.post("/create-post")
# This is how we handle the request body 
async def create_post(post: PostCreate, db: AsyncSession = Depends(get_db)) -> PostResponse: # The arrow is used to specify the return type
    try:
      new_post = Post(title=post.title, content=post.content, user_id=post.user_id) 
      db.add(new_post)
      await db.commit()
      return {
          "success": "true",
          "post": new_post
      }
    except Exception as e:
      raise HTTPException(status_code=500, detail=str(e))

@app.get("/get-all-posts")
#This is how we handle the query parameters
# limit is an optional parameter
# None is the default value if we want this field to be optional
async def get_posts(limit: int = None, db: AsyncSession = Depends(get_db)):
    try:
      query = select(Post)
      if limit:
        query = query.limit(limit)
      
      result = await db.execute(query)
      posts = result.scalars().all()

      return {
        "success": "true",
        "posts": posts
      }
    except Exception as e:
      raise HTTPException(status_code=500, detail=str(e))

@app.get("/posts/{post_id}")
async def get_post(post_id: int, db: AsyncSession = Depends(get_db)):
    try:
      query = select(Post).where(Post.id == post_id)
      result = await db.execute(query)
      post = result.scalar_one_or_none()

      if post is None:
        raise HTTPException(status_code=404, detail="Post not found")

      return {
        "success": "true",
        "post": post
      }
    except Exception as e:
      raise HTTPException(status_code=500, detail=str(e))

@app.delete("/delete-post/{post_id}")
async def delete_post(post_id: int, db: AsyncSession = Depends(get_db)):
  try:
    result = await db.execute(select(Post).where(Post.id == post_id))
    post = result.scalar_one_or_none()

    if post is None:
      raise HTTPException(status_code=404, detail="Post not found")

    await db.delete(post)
    await db.commit()

    return {
      "success": "true",
      "message": "Post deleted successfully"
    }
  except Exception as e:
    raise HTTPException(status_code=500, detail=str(e))

@app.put("/update-post/{post_id}")
async def update_post(post_id: int, body: PostCreate, db: AsyncSession = Depends(get_db)):
  try:
    result = await db.execute(select(Post).where(Post.id == post_id))
    post = result.scalar_one_or_none()

    if post is None:
      raise HTTPException(status_code=404, detail="Post not found")
    
    post.title = body.title
    post.content = body.content
    await db.commit()
    await db.refresh(post)

    return {
      "success": "true",
      "message": "Post updated successfully"
    }
  except Exception as e:
    raise HTTPException(status_code=500, detail=str(e))
