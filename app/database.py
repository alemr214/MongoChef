from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
from models.users_model import Users
from models.ingredients_model import Ingredients
from models.kitchen_tools_model import KitchenTools

# MongoDB connection settings
DATABASE_URL = "mongodb://localhost:27017"
DATABASE_NAME = "mongochef"
COLLECTIONS = [Users, Ingredients, KitchenTools]  # Collections to use and create


# Init connection to MongoDB with Beanie
async def init() -> AsyncIOMotorClient:
    """
    Initialize the MongoDB connection and Beanie ORM.

    Returns:
        AsyncIOMotorClient: The MongoDB client instance.
    """
    client = AsyncIOMotorClient(DATABASE_URL)
    db = client[DATABASE_NAME]
    await init_beanie(database=db, document_models=COLLECTIONS)
    return client  # Return the client for close use
