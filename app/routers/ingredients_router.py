from fastapi import APIRouter, HTTPException
from models.ingredients_model import Ingredients
from schemas.ingredients_schema import IngredientsBase
from pymongo.errors import DuplicateKeyError
from typing import List


router = APIRouter(prefix="/ingredients")


@router.get("/", response_model=List[Ingredients])
async def get_ingredients() -> List[Ingredients]:
    list_ingredients = await Ingredients.find_all().to_list()
    if not list_ingredients:
        raise HTTPException(status_code=404, detail="No ingredients found")
    return list_ingredients


@router.get("/{ingredient_name}", response_model=Ingredients)
async def get_ingredient_by_name(ingredient_name: str) -> Ingredients:
    existing_ingredient = await Ingredients.find_one(
        Ingredients.name == ingredient_name
    )
    if not existing_ingredient:
        raise HTTPException(status_code=404, detail="Ingredient not found")
    return existing_ingredient


@router.post("/create", response_model=Ingredients)
async def create_ingredient(ingredient: IngredientsBase) -> Ingredients:
    try:
        new_ingredient = Ingredients(**ingredient.model_dump())
        return new_ingredient
    except DuplicateKeyError:
        raise HTTPException(status_code=409, detail="Ingredient already exists")


@router.put("/update/{ingredient_name}", response_model=Ingredients)
async def update_ingredient(
    ingredient_name: str, ingredient: IngredientsBase
) -> Ingredients:
    existing_ingredient = await Ingredients.find_one(
        Ingredients.name == ingredient_name
    )

    if not existing_ingredient:
        raise HTTPException(status_code=404, detail="Ingredient not found")

    if ingredient.name and ingredient.name != existing_ingredient.name:
        existing_ingredient.name = ingredient.name
        await existing_ingredient.save()
    else:
        raise HTTPException(
            status_code=400,
            detail="Ingredient name cannot be empty or the same as the existing one",
        )

    return existing_ingredient


@router.delete("/delete/{ingredient_name}", response_model=Ingredients)
async def delete_ingredient(ingredient_name: str) -> Ingredients:
    existing_ingredient = await Ingredients.find_one(
        Ingredients.name == ingredient_name
    )

    if not existing_ingredient:
        raise HTTPException(status_code=404, detail="Ingredient not found")

    await existing_ingredient.delete()
    return existing_ingredient
