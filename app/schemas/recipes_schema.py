from pydantic import BaseModel, Field
from datetime import timedelta


class IngredientsDetail(BaseModel):
    """
    IngredientsDetail model for detailed information about ingredients.

    Attributes:
        - ingredients: Link[Ingredients]
        - quantity: int | float
        - unit: str
    """

    ingredients: str  # Placeholder for Link[Ingredients]
    quantity: int | float = Field(gt=0)
    unit: str = Field(min_length=1, max_length=20)


class RecipesBase(BaseModel):
    """
    Pydantic model for users validation in the endpoint

    Attributes:
        - title: str
        - ingredients: list[IngredientsDetail]
        - kitchen_tools: list[str]
        - portions: int
        - instructions: str
        - cooking_time: int
        - category: str
    """

    title: str = Field(min_length=1, max_length=70)
    ingredients: list[IngredientsDetail]
    kitchen_tools: list[str]  # Placeholder for Link[KitchenTools]
    portions: int = Field(gt=0)
    instructions: str = Field(min_length=1)
    cooking_time: timedelta  # Placeholder for timedelta
    category: str  # Placeholder for Link[Categories]
