from pydantic import BaseModel, Field


class CategoriesBase(BaseModel):
    """
    Pydantic model for recipes categories validation in the endpoint.

    Attributes:
        - name: str
        - description: str | None
    """

    name: str = Field(min_length=1, max_length=30)
    description: str | None = Field(max_length=100)
