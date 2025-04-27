from beanie import Document, Indexed
from pydantic import BaseModel
from typing import List
from datetime import timedelta


class IngredientsInfo(BaseModel):
    """
    Template for the ingredients model with Beanie linked to Recipes model.

    Attributes:
        id (str): Id of the ingredient.
        name (str): Name of the ingredient.
    """

    id: str
    name: str


class KitchenToolsInfo(BaseModel):
    """
    Template for the kitchen tools model with Beanie linked to Recipes model.

    Attributes:
        id (str): Id of the kitchen tool.
        name (str): Name of the kitchen tool.
    """

    id: str
    name: str


class CategoriesInfo(BaseModel):
    """
    Template for the categories model with Beanie linked to Recipes model.

    Attributes:
        id (str): Id of the category.
        name (str): Name of the category.
        description (str | None): Description of the category.
    """

    id: str
    name: str
    description: str | None = None


class IngredientsDetail(BaseModel):
    """
    Template for the ingredients attribute in the Recipes model adding the quantity and unit attributes.

    Attributes:
        ingredient_object (IngredientsInfo): Ingredient object.
        quantity (int | float): Quantity of the ingredient.
        unit (str): Unit of the ingredient.
    """

    ingredient_object: IngredientsInfo
    quantity: int | float
    unit: str


class Recipes(Document):
    """
    Recipe model with Beanie to save in a MongoDB database.

    Attributes:
        id (str): Id of the recipe.
        title (str): Title of the recipe.
        ingredients (List[IngredientsDetail]): List of ingredients with quantity and unit.
        kitchen_tools (List[KitchenToolsInfo]): List of kitchen tools.
        portions (int): Number of portions.
        instructions (str): Instructions to prepare the recipe.
        cooking_time (timedelta): Cooking time for the recipe.
        category (CategoriesInfo): Category of the recipe.
    """

    title: Indexed(str, unique=True)  # type: ignore
    ingredients: List[IngredientsDetail]
    kitchen_tools: List[KitchenToolsInfo]
    portions: int
    instructions: str
    cooking_time: timedelta
    category: CategoriesInfo
