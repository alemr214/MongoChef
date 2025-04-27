from fastapi import APIRouter, HTTPException
from typing import List
from pymongo.errors import DuplicateKeyError
from models.categories_model import Categories
from models.kitchen_tools_model import KitchenTools
from models.ingredients_model import Ingredients
from models.recipes_model import (
    CategoriesInfo,
    IngredientsDetail,
    IngredientsInfo,
    KitchenToolsInfo,
    Recipes,
)
from schemas.recipes_schema import RecipesBase
from datetime import timedelta
from utils.normalize import normalized_string


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

    Args
        recipes_title (str): The title of the recipe to retrieve.

    Raises:
        HTTPException: If the recipe is not found, a 404 Not Found error is raised.

    Returns:
        Recipes: The recipe object if found.
    """
    existing_recipe = await Recipes.find_one(
        Recipes.title == normalized_string(recipes_title)
    )
    if not existing_recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")
    return existing_recipe


@router.post("/create", response_model=Recipes)
async def create_recipe(recipe: RecipesBase) -> Recipes:
    """
    Create a new recipe in the database checking if the recipe already exists. Creating ingredients, kitchen tools and categories if they do not exist or use if they do.

    Args:
        recipe (RecipesBase): Recipe object model from the request body.

    Raises:
        HTTPException: If the recipe with the same title already exists, a 400 Bad Request error is raised.

    Returns:
        Recipes: The created recipe object.
    """
    # List to store the ingredients and kitchen tools dicts
    ingredients_list = []
    kitchen_tools_list = []

    # Check if the recipe already exists
    for ingredient in recipe.ingredients:
        ingredient_obj = await Ingredients.find_one(
            Ingredients.name == normalized_string(ingredient.name)
        )
        # If the ingredient does not exist, create it
        if not ingredient_obj:
            ingredient_obj = Ingredients(name=normalized_string(ingredient.name))
            await ingredient_obj.insert()

        # Append the ingredient object to the list
        ingredients_list.append(
            IngredientsDetail(
                ingredient_object=IngredientsInfo(
                    id=str(ingredient_obj.id),
                    name=normalized_string(ingredient_obj.name),
                ),
                quantity=ingredient.quantity,
                unit=normalized_string(ingredient.unit),
            )
        )

    # Check if the kitchen tool already exists
    for kitchen_tool in recipe.kitchen_tools:
        kitchen_tool_obj = await KitchenTools.find_one(
            KitchenTools.name == normalized_string(kitchen_tool.name)
        )
        # If the kitchen tool does not exist, create it
        if not kitchen_tool_obj:
            kitchen_tool_obj = KitchenTools(name=normalized_string(kitchen_tool.name))
            await kitchen_tool_obj.insert()

        # Append the kitchen tool object to the list
        kitchen_tools_list.append(
            KitchenToolsInfo(
                id=str(kitchen_tool_obj.id),
                name=normalized_string(kitchen_tool_obj.name),
            )
        )

    # Check if the category already exists
    category_obj = await Categories.find_one(
        Categories.name == normalized_string(recipe.category.name)
    )
    # If the category does not exist, create it
    if not category_obj:
        category_obj = Categories(
            name=normalized_string(recipe.category.name), description=None
        )
        await category_obj.insert()
    # Create the category info object
    category_info = CategoriesInfo(
        id=str(category_obj.id),
        name=normalized_string(category_obj.name),
        description=category_obj.description,
    )

    # Create the recipe object
    recipe_obj = Recipes(
        title=normalized_string(recipe.title),
        ingredients=ingredients_list,
        kitchen_tools=kitchen_tools_list,
        portions=recipe.portions,
        instructions=recipe.instructions,
        cooking_time=timedelta(minutes=recipe.cooking_time),
        category=category_info,
    )

    try:
        await recipe_obj.insert()
        return recipe_obj
    except DuplicateKeyError:
        raise HTTPException(
            status_code=400, detail="Recipe with this title already exists"
        )


@router.put("/update/{recipe_title}", response_model=Recipes)
async def update_recipe(recipe_title: str, recipe: RecipesBase) -> Recipes:
    """
    Update an existing recipe in the database.

    Args:
        recipe_title (str): The title of the recipe to update.
        recipe (RecipesBase): The updated recipe object.

    Raises:
        HTTPException: The recipe with the given title does not exist, a 404 Not Found error is raised.
        HTTPException: If another recipe with the same title already exists, a 400 Bad Request error is raised.

    Returns:
        Recipes: The updated recipe object.
    """
    # Find the existing recipe by title
    existing_recipe = await Recipes.find_one(
        Recipes.title == normalized_string(recipe_title)
    )
    if not existing_recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")

    ingredients_list = []
    for ingredient in recipe.ingredients:
        name_norm = normalized_string(ingredient.name)
        # Check if the ingredient already exists
        ingr_obj = await Ingredients.find_one(Ingredients.name == name_norm)
        if not ingr_obj:
            # If the ingredient does not exist, create it
            ingr_obj = Ingredients(name=name_norm)
            await ingr_obj.insert()

        # Append the ingredient object to the list
        ingredients_list.append(
            IngredientsDetail(
                ingredient_object=IngredientsInfo(
                    id=str(ingr_obj.id),
                    name=ingr_obj.name,
                ),
                quantity=ingredient.quantity,
                unit=normalized_string(ingredient.unit),
            )
        )

    kitchen_tools_list = []
    for tool in recipe.kitchen_tools:
        tool_name = normalized_string(tool.name)
        # Check if the kitchen tool already exists
        tool_obj = await KitchenTools.find_one(KitchenTools.name == tool_name)
        if not tool_obj:
            # If the kitchen tool does not exist, create it
            tool_obj = KitchenTools(name=tool_name)
            await tool_obj.insert()

        # Append the kitchen tool object to the list
        kitchen_tools_list.append(
            KitchenToolsInfo(
                id=str(tool_obj.id),
                name=tool_obj.name,
            )
        )

    cat_name = normalized_string(recipe.category.name)
    # Check if the category already exists
    cat_obj = await Categories.find_one(Categories.name == cat_name)
    if not cat_obj:
        # If the category does not exist, create it
        cat_obj = Categories(name=cat_name, description=None)
        await cat_obj.insert()

    # Create the category info object
    category_info = CategoriesInfo(
        id=str(cat_obj.id),
        name=cat_obj.name,
        description=cat_obj.description,
    )

    # Update the existing recipe with the new values
    existing_recipe.title = normalized_string(recipe.title)
    existing_recipe.ingredients = ingredients_list
    existing_recipe.kitchen_tools = kitchen_tools_list
    existing_recipe.portions = recipe.portions
    existing_recipe.instructions = recipe.instructions
    existing_recipe.cooking_time = timedelta(minutes=recipe.cooking_time)
    existing_recipe.category = category_info

    # Save the updated recipe to the database
    try:
        await existing_recipe.save()
        return existing_recipe
    except DuplicateKeyError:
        raise HTTPException(
            status_code=400, detail="Another recipe with this title already exists"
        )


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
