from src.database.db import Base
from sqlalchemy import Column, Integer, String, ForeignKey, Text, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

class User(Base):
  __tablename__="users"

  id = Column(Integer, primary_key=True, index=True)
  username = Column(String, unique=True, nullable=False)
  email = Column(String, unique=True, nullable=False)
  created_at = Column(DateTime(timezone=True), server_default=func.now())

  #Relationship with POST
  posts = relationship("Post", back_populates="owner")

class Post(Base):
  __tablename__= "posts"

  id = Column(Integer, primary_key=True, index=True)
  title = Column(String, nullable=False)
  content = Column(Text, nullable=False)
  created_at = Column(DateTime(timezone=True), server_default=func.now())

  # Foreign Key
  user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

  #Relationship to user
  owner = relationship("User", back_populates="posts")