from pydantic import BaseModel, Field
from typing import Optional


class CommentUser(BaseModel):
    id: int = Field(..., ge=1, description="ID пользователя")
    username: str = Field(..., max_length=255, description="Имя пользователя")


class CommentBase(BaseModel):
    body: Optional[str] = Field(None, description="Текст комментария")
    postId: Optional[int] = Field(None, ge=1, description="ID поста")


class CommentCreate(CommentBase):
    body: str = Field(..., description="Комментарий обязателен")
    postId: int = Field(..., ge=1, description="ID поста обязателен")


class CommentUpdate(CommentBase):
    pass  # Все поля опциональны для обновления


class CommentGet(BaseModel):
    id: int = Field(..., ge=1, description="ID комментария")
    body: str = Field(..., description="Текст комментария")
    postId: int = Field(..., ge=1, description="ID поста")
    user: CommentUser