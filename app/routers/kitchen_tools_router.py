from fastapi import APIRouter, HTTPException
from models.kitchen_tools_model import KitchenTools
from schemas.kitchen_tools_schema import KitchenToolsBase
from pymongo.errors import DuplicateKeyError
from typing import List


router = APIRouter(prefix="/kitchen_tools")


@router.get("/", response_model=List[KitchenTools])
async def get_kitchen_tools() -> List[KitchenTools]:
    """
    Get all kitchen tools stored in the database in a list.

    Raises:
        HTTPException: If no kitchen tools are found, a 404 error is raised.

    Returns:
        List[KitchenTools]: A list of all kitchen tools.
    """
    list_kitchen_tools = await KitchenTools.find_all().to_list()
    if not list_kitchen_tools:
        raise HTTPException(status_code=404, detail="No kitchen tools found")
    return list_kitchen_tools


@router.get("/{kitchen_tool_name}", response_model=KitchenTools)
async def get_kitchen_tool_by_name(kitchen_tool_name: str) -> KitchenTools:
    """
    Get a kitchen tool by its name.

    Args:
        kitchen_tool_name (str): The name of the kitchen tool to retrieve.

    Raises:
        HTTPException: If the kitchen tool is not found, a 404 error is raised.

    Returns:
        KitchenTools: The kitchen tool object if found.
    """
    existing_kitchen_tool = await KitchenTools.find_one(
        KitchenTools.name == kitchen_tool_name
    )
    if not existing_kitchen_tool:
        raise HTTPException(status_code=404, detail="Kitchen tool not found")
    return existing_kitchen_tool


@router.post("/create", response_model=KitchenTools)
async def create_kitchen_tool(kitchen_tool: KitchenToolsBase) -> KitchenTools:
    """
    Create a new kitchen tool.

    Args:
        kitchen_tool (KitchenToolsBase): The kitchen tool object model from Pydantic schema.

    Raises:
        HTTPException: If the kitchen tool already exists, a 409 error is raised.

    Returns:
        KitchenTools: The created kitchen tool object from Beanie model.
    """
    try:
        new_kitchen_tool = KitchenTools(**kitchen_tool.model_dump())
        await new_kitchen_tool.insert()
        return new_kitchen_tool
    except DuplicateKeyError:
        raise HTTPException(status_code=409, detail="Kitchen tool already exists")


@router.put("/update/{kitchen_tool_name}", response_model=KitchenTools)
async def update_kitchen_tool(
    kitchen_tool_name: str, kitchen_tool: KitchenToolsBase
) -> KitchenTools:
    """
    Update and existing kitchen tool by its name.

    Args:
        kitchen_tool_name (str): The name of the kitchen tool to update
        kitchen_tool (KitchenToolsBase): The kitchen tool object model from Pydantic schema.

    Raises:
        HTTPException: If the kitchen tool is not found, a 404 error is raised.
        HTTPException: If the kitchen tool name is empty or the same as the existing one, a 400 error is raised.

    Returns:
        KitchenTools: The updated kitchen tool object from beanie model.
    """
    existing_kitchen_tool = await KitchenTools.find_one(
        KitchenTools.name == kitchen_tool_name
    )

    if not existing_kitchen_tool:
        raise HTTPException(status_code=404, detail="kitchen_tool not found")

    if kitchen_tool.name and kitchen_tool.name != existing_kitchen_tool.name:
        existing_kitchen_tool.name = kitchen_tool.name
        await existing_kitchen_tool.save()
    else:
        raise HTTPException(
            status_code=400,
            detail="Kitchen tool name cannot be empty or the same as the existing one",
        )

    return existing_kitchen_tool


# DELETE kitchen tool by name.
@router.delete("/delete/{kitchen_tool_name}", response_model=KitchenTools)
async def delete_kitchen_tool(kitchen_tool_name: str) -> KitchenTools:
    """
    Delete a kitchen tool by its name.

    Args:
        kitchen_tool_name (str): The name of the kitchen tool to delete

    Raises:
        HTTPException: If the kitchen tool is not found, a 404 error is raised.

    Returns:
        KitchenTools: The deleted kitchen tool object from Beanie model into the database.
    """
    existing_kitchen_tool = await KitchenTools.find_one(
        KitchenTools.name == kitchen_tool_name
    )

    if not existing_kitchen_tool:
        raise HTTPException(status_code=404, detail="Kitchen tool not found")

    await existing_kitchen_tool.delete()
    return existing_kitchen_tool
