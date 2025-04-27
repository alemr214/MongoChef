from fastapi import APIRouter, HTTPException
from models.ingredients_model import Ingredients
from schemas.ingredients_schema import IngredientsBase
from pymongo.errors import DuplicateKeyError
from typing import List
from utils.normalize import normalized_string


router = APIRouter(prefix="/ingredients")


# GET all ingredients.
@router.get("/", response_model=List[Ingredients])
async def get_ingredients() -> List[Ingredients]:
    """
    Get all ingredients stored in the database.

    Raises:
        HTTPException: If no ingredients are found, a 404 error is raised.

    Returns:
        List[Ingredients]: A list of all ingredients.
    """
    list_ingredients = await Ingredients.find_all().to_list()
    if not list_ingredients:
        raise HTTPException(status_code=404, detail="No ingredients found")
    return list_ingredients


# GET ingredient by name.
@router.get("/{ingredient_name}", response_model=Ingredients)
async def get_ingredient_by_name(ingredient_name: str) -> Ingredients:
    """
    Get an ingredient by its name.

    Args:
        ingredient_name (str): The name of the ingredient to retrieve.

    Raises:
        HTTPException: If the ingredient is not found, a 404 error is raised.

    Returns:
        Ingredients: The ingredient object if found.
    """
    existing_ingredient = await Ingredients.find_one(
        Ingredients.name == normalized_string(ingredient_name)
    )
    if not existing_ingredient:
        raise HTTPException(status_code=404, detail="Ingredient not found")
    return existing_ingredient


# POST create a new ingredient.
@router.post("/create", response_model=Ingredients)
async def create_ingredient(ingredient: IngredientsBase) -> Ingredients:
    """
    Create a new ingredient.

    Args:
        ingredient (IngredientsBase): The ingredient object model from Pydantic schema.

    Raises:
        HTTPException: If the ingredient already exists, a 409 error is raised.

    Returns:
        Ingredients: The newly created ingredient object from Beanie model.
    """
    try:
        new_ingredient = Ingredients(**ingredient.model_dump())
        new_ingredient.name = normalized_string(new_ingredient.name)
        await new_ingredient.insert()
        return new_ingredient
    except DuplicateKeyError:
        raise HTTPException(status_code=409, detail="Ingredient already exists")


# PUT update an existing ingredient.
@router.put("/update/{ingredient_name}", response_model=Ingredients)
async def update_ingredient(
    ingredient_name: str, ingredient: IngredientsBase
) -> Ingredients:
    """
    Update an existing ingredient.

    Args:
        ingredient_name (str): The name of the ingredient to update.
        ingredient (IngredientsBase): The updated ingredient object model from Pydantic schema.

    Raises:
        HTTPException: If the ingredient is not found, a 404 error is raised.
        HTTPException: If the ingredient name is empty or the same as the existing one, a 400 error is raised.

    Returns:
        Ingredients: The updated ingredient object from Beanie model.
    """
    existing_ingredient = await Ingredients.find_one(
        Ingredients.name == normalized_string(ingredient_name)
    )

    if not existing_ingredient:
        raise HTTPException(status_code=404, detail="Ingredient not found")

    if ingredient.name and ingredient.name != existing_ingredient.name:
        existing_ingredient.name = normalized_string(ingredient.name)
        await existing_ingredient.save()
    else:
        raise HTTPException(
            status_code=400,
            detail="Ingredient name cannot be empty or the same as the existing one",
        )

    return existing_ingredient


# DELETE an ingredient.
@router.delete("/delete/{ingredient_name}", response_model=Ingredients)
async def delete_ingredient(ingredient_name: str) -> Ingredients:
    """
    Delete an ingredient by its name.

    Args:
        ingredient_name (str): The name of the ingredient to delete.

    Raises:
        HTTPException: If the ingredient is not found, a 404 error is raised.

    Returns:
        Ingredients: The deleted ingredient object from Beanie model into the database.
    """
    existing_ingredient = await Ingredients.find_one(
        Ingredients.name == normalized_string(ingredient_name)
    )

    if not existing_ingredient:
        raise HTTPException(status_code=404, detail="Ingredient not found")

    await existing_ingredient.delete()
    return existing_ingredient
