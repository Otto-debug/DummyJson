from pydantic import BaseModel, Field
from typing import List, Optional

class Reactions(BaseModel):
    likes: int
    dislikes: int


class PostBase(BaseModel):
    title: Optional[str] = Field(None, max_length=255, description="Title of the post")
    body: Optional[str] = Field(None, description="Content of the post")
    userId: Optional[int] = Field(None, ge=1, description="ID of the user who created the post")
    tags: Optional[List[str]] = Field(default_factory=list, description="Tags associated with the post")
    # reactions: Optional[dict] = Field(0, ge=0, description="Number of reactions to the post")
    reactions: Reactions


class PostCreate(PostBase):
    title: str = Field(..., max_length=255, description="Title is required")
    body: str = Field(..., description="Body is required")
    userId: int = Field(..., ge=1, description="User ID is required")
    tags: List[str] = Field(default_factory=list, description="Tags are required (can be empty list)")
    reactions: Reactions

class PostUpdate(PostBase):
    pass  # inherits optional fields from PostBase


class PostGet(BaseModel):
    id: int = Field(..., ge=1, description="Unique identifier for the post")
    title: str = Field(..., max_length=255)
    body: str = Field(...)
    userId: int = Field(..., ge=1)
    tags: List[str] = Field(default_factory=list)
    # reactions: int = Field(default=0, ge=0)
    reactions: Reactions