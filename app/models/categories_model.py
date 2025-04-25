from beanie import Document, Indexed


class Categories(Document):
    """
    Recipes category model extends from Document for MongoDB template with Beanie ODM.

    Attributes:
        - name: str
        - description: str | None
    """

    name: Indexed(str, unique=True)  # type: ignore
    description: str | None = None

    class Settings:
        name = "categories"
