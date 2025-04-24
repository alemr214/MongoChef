from beanie import Document, Indexed


class KitchenTools(Document):
    """
    Kitchen Tools model extends from Document for MongoDB template with Beanie ORM.

    Attributes:
        - name: str
    """

    name: Indexed(str, unique=True)  # type: ignore

    class Settings:
        name = "kitchen_tools"
