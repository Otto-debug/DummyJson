from pydantic import BaseModel, Field
from typing import Optional


class TodoBase(BaseModel):
    todo: Optional[str] = Field(None, max_length=255, description="Описание задачи")
    completed: Optional[bool] = Field(default=False, description="Статус выполнения задачи")
    userId: Optional[int] = Field(None, ge=1, description="ID пользователя, которому принадлежит задача")


# -------- Схема для создания --------
class TodoCreate(TodoBase):
    todo: str = Field(..., max_length=255, description="Описание задачи обязательно")
    userId: int = Field(..., ge=1, description="ID пользователя обязателен")
    completed: Optional[bool] = Field(default=False, description="Можно передать статус выполнения")


# -------- Схема для обновления --------
class TodoUpdate(TodoBase):
    pass  # Все поля опциональны для частичного обновления


# -------- Схема для получения --------
class TodoGet(TodoBase):
    id: int = Field(..., ge=1, description="Уникальный ID задачи")
    todo: str
    completed: bool
    userId: int


# -------- Схема для удаления --------
class TodoDelete(TodoGet):
    pass  # API возвращает удалённую сущность, аналогично GET

