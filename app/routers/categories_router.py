from fastapi import APIRouter, HTTPException
from models.categories_model import Categories
from schemas.categories_schema import CategoriesBase
from pymongo.errors import DuplicateKeyError
from typing import List
from utils.normalize import normalized_string

router = APIRouter(prefix="/categories")


@router.get("/", response_model=List[Categories])
async def get_categories() -> List[Categories]:
    """
    Get all categories stored in the database in a list.

    Raises:
        HTTPException: If no categories are found, a 404 error is raised.

    Returns:
        List[Categories]: A list of all categories.
    """
    list_categories = await Categories.find_all().to_list()
    if not list_categories:
        raise HTTPException(status_code=404, detail="No categories found")
    return list_categories


@router.get("/{category_name}", response_model=Categories)
async def get_category_by_name(category_name: str) -> Categories:
    """
    Get a category by its name.

    Args:
        category_name (str): The name of the category to retrieve.

    Raises:
        HTTPException: If the category is not found, a 404 error is raised.

    Returns:
        Categories: The category object if found.
    """
    existing_category = await Categories.find_one(
        Categories.name == normalized_string(category_name)
    )
    if not existing_category:
        raise HTTPException(status_code=404, detail="Category not found")
    return existing_category


@router.post("/create", response_model=Categories)
async def create_category(category: CategoriesBase) -> Categories:
    """
    Create a new category.

    Args:
        category (CategoriesBase): The category object model from Pydantic schema.

    Raises:
        HTTPException: If the category already exists, a 409 error is raised.

    Returns:
        Categories: The created category object from Beanie model.
    """
    try:
        new_category = Categories(**category.model_dump())
        new_category.name = normalized_string(category.name)
        await new_category.create()
        return new_category
    except DuplicateKeyError:
        raise HTTPException(status_code=409, detail="Category already exists")


@router.put("/update/{category_name}", response_model=Categories)
async def update_category(category_name: str, category: CategoriesBase) -> Categories:
    """
    Update and existing category by its name.

    Args:
        category_name (str): The name of the category to update
        category (CategoriesBase): The category object model from Pydantic schema.

    Raises:
        HTTPException: If the category is not found, a 404 error is raised.
        HTTPException: If the category name is empty or the same as the existing one, a 400 error is raised.

    Returns:
        Categories: The updated category object from beanie model.
    """
    existing_category = await Categories.find_one(
        Categories.name == normalized_string(category_name)
    )

    if not existing_category:
        raise HTTPException(status_code=404, detail="category not found")

    update_data = category.model_dump()

    if not update_data:
        raise HTTPException(status_code=400, detail="No data provided for update")

    for field, value in update_data.items():
        setattr(existing_category, field, value)

    existing_category.name = normalized_string(category.name)
    await existing_category.save()
    return existing_category


# DELETE category by name.
@router.delete("/delete/{category_name}", response_model=Categories)
async def delete_category(category_name: str) -> Categories:
    """
    Delete a category by its name.

    Args:
        category_name (str): The name of the category to delete

    Raises:
        HTTPException: If the category is not found, a 404 error is raised.

    Returns:
        Categories: The deleted category object from Beanie model into the database.
    """
    existing_category = await Categories.find_one(
        Categories.name == normalized_string(category_name)
    )

    if not existing_category:
        raise HTTPException(status_code=404, detail="Category not found")

    await existing_category.delete()
    return existing_category
