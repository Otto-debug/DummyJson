from pydantic import BaseModel, Field, HttpUrl
from typing import List, Optional, Literal

# Общий список допустимых mealType, включая "Beverage"
MealType = Literal["Breakfast", "Lunch", "Dinner", "Snack", "Dessert", "Beverage"]

class RecipeBase(BaseModel):
    name: Optional[str]
    ingredients: Optional[List[str]]
    instructions: Optional[List[str]]
    prepTimeMinutes: Optional[int]
    cookTimeMinutes: Optional[int]
    servings: Optional[int]
    difficulty: Optional[Literal["Easy", "Medium", "Hard"]]
    cuisine: Optional[str]
    caloriesPerServing: Optional[int]
    tags: Optional[List[str]]
    image: Optional[HttpUrl]
    mealType: Optional[List[MealType]]

class RecipePOST(RecipeBase):
    name: str
    ingredients: List[str]
    instructions: List[str]
    prepTimeMinutes: int
    cookTimeMinutes: int
    servings: int
    difficulty: Literal["Easy", "Medium", "Hard"]
    cuisine: str
    caloriesPerServing: int
    tags: List[str]
    image: HttpUrl
    mealType: List[MealType]
    userId: int

class RecipePUT(RecipeBase):
    pass  # Все поля уже optional в базовом классе

class RecipeGET(BaseModel):
    id: int
    name: str
    ingredients: List[str]
    instructions: List[str]
    prepTimeMinutes: int
    cookTimeMinutes: int
    servings: int
    difficulty: Literal["Easy", "Medium", "Hard"]
    cuisine: str
    caloriesPerServing: int
    tags: List[str]
    image: HttpUrl
    mealType: List[MealType]
    userId: int
    rating: float = Field(..., ge=0, le=5)
    reviewCount: int

class RecipeShort(BaseModel):
    id: int
    name: str
