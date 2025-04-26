from beanie import Document, Indexed, Link
from typing import List
from datetime import timedelta
from pydantic import BaseModel

from .categories_model import Categories
from .ingredients_model import Ingredients
from .kitchen_tools_model import KitchenTools


class IngredientsDetail(BaseModel):
    """
    IngredientsDetail model for detailed information about ingredients.

    Attributes:
        - ingredients: Link[Ingredients]
        - quantity: int | float
        - unit: str
    """

    ingredients: Link[Ingredients]
    quantity: int | float
    unit: str


class Recipes(Document):
    """
    Recipes model extends from Document for MongoDB template with Beanie ODM.

    Attributes:
        - title: str
        - ingredients: List[IngredientsDetail]
        - kitchen_tools: List[Link[KitchenTools]]
        - portions: int
        - instructions: str
        - cooking_time: timedelta
        - category: Link[Categories]
    """

    title: Indexed(str, unique=True)  # type: ignore
    ingredients: List[IngredientsDetail]
    kitchen_tools: List[Link[KitchenTools]]
    portions: int
    instructions: str
    cooking_time: timedelta
    category: Link[Categories]

    class Settings:
        name = "recipes"
