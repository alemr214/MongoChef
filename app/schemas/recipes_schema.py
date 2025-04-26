from pydantic import BaseModel, Field
from typing import List


class IngredientsBaseDetail(BaseModel):
    """
    IngredientsBaseDetail is a Pydantic model that represents the details of an ingredient.

    Attributes:
        name (str): The name of the ingredient.
        quantity (int): The quantity of the ingredient.
        unit (str): The unit of measurement for the ingredient.
    """

    name: str
    quantity: int
    unit: str


class KitchenToolsBaseInfo(BaseModel):
    """
    KitchenToolsBaseInfo is a Pydantic model that represents the information of kitchen tools.

    Attributes:
        name (str): The name of the kitchen tools
    """

    name: str


class CategoriesBaseInfo(BaseModel):
    """
    CategoriesBaseInfo is a Pydantic model that represents the information of recipe categories.

    Attributes:
        name (str): The name of the recipe category.
    """

    name: str


class RecipesBase(BaseModel):
    """
    RecipesBase is a Pydantic model that represents the base information of a recipe.

    Attributes:
        title (str): The title of the recipe.
        ingredients (List[IngredientsBaseDetail]): A list of ingredients required for the recipe.
        kitchen_tools (List[KitchenToolsBaseInfo]): A list of kitchen tools required for the recipe.
        portions (int): The number of portions the recipe serves.
        instructions (str): The instructions for preparing the recipe.
        cooking_time (int): The time required to cook the recipe in minutes.
        category (CategoriesBaseInfo): The category of the recipe.
    """

    title: str = Field(min_length=1, max_length=50)
    ingredients: List[IngredientsBaseDetail]
    kitchen_tools: List[KitchenToolsBaseInfo]
    portions: int = Field(gt=1)
    instructions: str = Field(min_length=1)
    cooking_time: int = Field(gt=0)
    category: CategoriesBaseInfo
