from pydantic import BaseModel

class UserCreate(BaseModel):
  username: str
  email: str

class UserRespone(BaseModel):
  success: bool
  message: str

class PostCreate(BaseModel):
  title: str
  content: str
  user_id: int 

class PostResponse(BaseModel):
  success: bool
  post: PostCreate
