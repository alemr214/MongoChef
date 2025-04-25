from pydantic import BaseModel, Field


class IngredientsBase(BaseModel):
    """
    Pydantic model for ingredient validation in the endpoint.

    Attributes:
        - name: str
    """

    name: str = Field(min_length=1, max_length=30)
