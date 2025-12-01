from fastapi import FastAPI, HTTPException
from src.schemas import Post, PostResponse

app = FastAPI()

posts = {
    1 : {"title": "Post 1", "content": "Content of Post 1"},
    2 : {"title": "Post 2", "content": "Content of Post 2"},
    3 : {"title": "Post 3", "content": "Content of Post 3"},
    3 : {"title": "Post 3", "content": "Content of Post 3"},
    4 : {"title": "Post 4", "content": "Content of Post 4"},
    5 : {"title": "Post 5", "content": "Content of Post 5"},
    6 : {"title": "Post 6", "content": "Content of Post 6"},
    7 : {"title": "Post 7", "content": "Content of Post 7"},
    8 : {"title": "Post 8", "content": "Content of Post 8"},
    9 : {"title": "Post 9", "content": "Content of Post 9"},
    10 : {"title": "Post 10", "content": "Content of Post 10"},
}

@app.get("/")
def hello_world():
    return {
        "success": "true",
        "message": "Hello World" # This data will be automatically converted to JSON
    }

@app.get("/posts")
#This is how we handle the query parameters
# limit is an optional parameter
# None is the default value if we want this field to be optional
def get_posts(limit: int = None):
    if limit:
        return{
            "success": "true",
            "posts": list(posts.values())[:limit]
        }
    return {
        "success": "true",
        "posts": posts
    }

@app.get("/posts/{post_id}")
def get_post(post_id: int):
    if post_id not in posts:
        raise HTTPException(status_code=404, detail="Post not found")
    return {
        "success": "true",
        "post": posts.get(post_id)
    }

@app.post("/posts")
# This is how we handle the request body 
def create_post(post: Post) -> PostResponse: # The arrow is used to specify the return type
    new_post = {"title": post.title, "content": post.content}
    posts[max(posts.keys()) + 1] = new_post
    return {
        "success": "true",
        "post": new_post
    }