from fastapi import APIRouter, HTTPException
from models.kitchen_tools_model import KitchenTools
from schemas.kitchen_tools_schema import KitchenToolsBase
from pymongo.errors import DuplicateKeyError
from typing import List


router = APIRouter(prefix="/kitchen_tools")


@router.get("/", response_model=List[KitchenTools])
async def get_kitchen_tools() -> List[KitchenTools]:
    list_kitchen_tools = await KitchenTools.find_all().to_list()
    if not list_kitchen_tools:
        raise HTTPException(status_code=404, detail="No kitchen tools found")
    return list_kitchen_tools


@router.get("/{kitchen_tool_name}", response_model=KitchenTools)
async def get_kitchen_tool_by_name(kitchen_tool_name: str) -> KitchenTools:
    existing_kitchen_tool = await KitchenTools.find_one(
        KitchenTools.name == kitchen_tool_name
    )
    if not existing_kitchen_tool:
        raise HTTPException(status_code=404, detail="Kitchen tool not found")
    return existing_kitchen_tool


@router.post("/create", response_model=KitchenTools)
async def create_kitchen_tool(kitchen_tool: KitchenToolsBase) -> KitchenTools:
    try:
        new_kitchen_tool = KitchenTools(**kitchen_tool.model_dump())
        return new_kitchen_tool
    except DuplicateKeyError:
        raise HTTPException(status_code=409, detail="Kitchen tool already exists")


@router.put("/update/{kitchen_tool_name}", response_model=KitchenTools)
async def update_kitchen_tool(
    kitchen_tool_name: str, kitchen_tool: KitchenToolsBase
) -> KitchenTools:
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


@router.delete("/delete/{kitchen_tool_name}", response_model=KitchenTools)
async def delete_kitchen_tool(kitchen_tool_name: str) -> KitchenTools:
    existing_kitchen_tool = await KitchenTools.find_one(
        KitchenTools.name == kitchen_tool_name
    )

    if not existing_kitchen_tool:
        raise HTTPException(status_code=404, detail="Kitchen tool not found")

    await existing_kitchen_tool.delete()
    return existing_kitchen_tool
