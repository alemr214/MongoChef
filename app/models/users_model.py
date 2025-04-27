from beanie import Document, Indexed, Link
from pydantic import EmailStr


class Users(Document):
    """
    Users model extends from Document for MongoDB template with Beanie ODM.

    Attributes:
        - name: str
        - lastname1: str
        - lastname2: str | None
        - email: EmailStr (unique=True)
        - favorite_recipes: List[Link[Recipes]]
    """

    name: str
    lastname1: str
    lastname2: str | None
    email: Indexed(EmailStr, unique=True)  # type: ignore

    class Settings:
        name = "users"
