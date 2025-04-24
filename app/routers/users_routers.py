from fastapi import APIRouter, HTTPException
from pydantic import EmailStr
from pymongo.errors import DuplicateKeyError
from app.models.users_model import Users
from schemas.users_schema import UsersBase

from typing import List


router = APIRouter(prefix="/users")


# Get all users in the database
@router.get("/", response_model=List[Users])
async def get_users() -> List[Users]:
    """
    Get all users from the database.

    Returns:
        List[Users]: A list of user objects.
    """
    list_users = await Users.find_all().to_list()
    return list_users


# Get a user by their email address
@router.get("/{user_email}", response_model=Users)
async def get_user_by_email(user_email: EmailStr) -> Users:
    """
    Return a user by their email address.

    Args:
        user_email (EmailStr): The email address of the user to retrieve.

    Returns:
        Users: The user object if found.
    """
    existing_user = await Users.find_one(Users.email == user_email)
    return existing_user


# Create a new user in the database
@router.post("/create", response_model=Users)
async def create_user(user: UsersBase) -> Users:
    """
    Create a new user in the database.

    Args:
        user (UsersBase): The user object to create.

    Raises:
        HTTPException: If the user already exists. If the user already exists, a 409 Conflict error is raised.

    Returns:
        Users: The created user object.
    """
    try:
        new_user = Users(**user.model_dump())
        await new_user.insert()
        return new_user
    except DuplicateKeyError:
        raise HTTPException(status_code=409, detail="User already exists")


# Update a user in the database
@router.put("/update/{user_email}", response_model=Users)
async def update_user(user_email: EmailStr, user: UsersBase) -> Users:
    """
    Update a user in the database with new user model data.

    Args:
        user_email (EmailStr): The email address of the user to update.
        user (UsersBase): The user object with updated data.

    Raises:
        HTTPException: If the user is not found, a 404 Not Found error is raised.
        HTTPException: If no data is provided for update, a 400 Bad Request error is raised.

    Returns:
        Users: The updated user object.
    """
    existing_user = await Users.find_one(Users.email == user_email)

    if not existing_user:
        raise HTTPException(status_code=404, detail="User not found")

    update_data = user.model_dump()

    if not update_data:
        raise HTTPException(status_code=400, detail="No data to update")

    for field, value in update_data.items():
        setattr(existing_user, field, value)

    await existing_user.save()
    return existing_user


# Delete a user from the database
@router.delete("/delete/{user_email}", response_model=Users)
async def delete_user(user_email: EmailStr) -> Users:
    """
    Delete a user from the database by their email address.

    Args:
        user_email (EmailStr): The email address of the user to delete.

    Raises:
        HTTPException: If the user is not found, a 404 Not Found error is raised.

    Returns:
        Users: The deleted user object.
    """
    existing_user = await Users.find_one(Users.email == user_email)
    if not existing_user:
        raise HTTPException(status_code=404, detail="User not found")
    await existing_user.delete()
    return existing_user
