from fastapi import APIRouter, HTTPException
from typing import List
from pymongo.errors import DuplicateKeyError
from models.recipes_model import Recipes
from schemas.recipes_schema import RecipesBase


router = APIRouter(prefix="/recipes")


@router.get("/", response_model=List[Recipes])
async def get_all_recipes() -> List[Recipes]:
    """
    Get all recipes from the database.

    Raises:
        HTTPException: If no recipes are found, a 404 Not Found error is raised.

    Returns:
        List[Recipes]: A list of recipe objects.
    """
    recipes = await Recipes.find_all().to_list()
    if not recipes:
        raise HTTPException(status_code=404, detail="No recipes found")
    return recipes


@router.get("/{recipes_title}", response_model=Recipes)
async def get_recipe_by_title(recipes_title: str) -> Recipes:
    """
    Get a recipe by its title.

    Args:
        recipes_title (str): The title of the recipe to retrieve.

    Raises:
        HTTPException: If the recipe is not found, a 404 Not Found error is raised.

    Returns:
        Recipes: The recipe object if found.
    """
    recipe = await Recipes.find_one({"title": recipes_title})
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")
    return recipe


@router.post("/create", response_model=Recipes)
async def create_recipe(recipe: RecipesBase) -> Recipes:
    """
    Create a new recipe in the database.

    Args:
        recipe (RecipesBase): The recipe object to create.

    Raises:
        HTTPException: If the recipe already exists, a 409 Conflict error is raised.

    Returns:
        Recipes: The created recipe object.
    """
    try:
        new_recipe = await Recipes(**recipe.model_dump())
        await new_recipe.insert()
        return new_recipe
    except DuplicateKeyError:
        raise HTTPException(status_code=409, detail="Recipe already exists")


@router.put("/update/{recipe_title}")
async def update_recipe(recipe_title: str, recipe: RecipesBase) -> Recipes:
    """
    Update an existing recipe in the database.

    Args:
        recipe_title (str): The title of the recipe to update.
        recipe (RecipesBase): The recipe object with updated data.

    Raises:
        HTTPException: If the recipe is not found, a 404 Not Found error is raised.
        HTTPException: If no data is provided for update, a 400 Bad Request error is raised.

    Returns:
        Recipes: The updated recipe object.
    """
    existing_recipe = await Recipes.find_one(Recipes.title == recipe_title)

    if not existing_recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")

    updated_data = recipe.model_dump()

    if not updated_data:
        raise HTTPException(status_code=400, detail="No data provided for update")

    for field, value in updated_data.items():
        setattr(existing_recipe, field, value)

    await existing_recipe.save()
    return existing_recipe


@router.delete("/delete/{recipe_title}", response_model=Recipes)
async def delete_recipe(recipe_title: str) -> Recipes:
    """
    Delete a recipe from the database.

    Args:
        recipe_title (str): The title of the recipe to delete.

    Raises:
        HTTPException: If the recipe is not found, a 404 Not Found error is raised.

    Returns:
        Recipes: The deleted recipe object.
    """
    existing_recipe = await Recipes.find_one(Recipes.title == recipe_title)
    if not existing_recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")
    await existing_recipe.delete()
    return existing_recipe
