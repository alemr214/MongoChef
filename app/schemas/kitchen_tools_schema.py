from pydantic import BaseModel, Field


class KitchenToolsBase(BaseModel):
    """
    Pydantic model for kitchen tools validation in the endpoint.

    Attributes:
        - name: str
    """

    name: str = Field(min_length=1, max_length=30)
