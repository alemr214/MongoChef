from pydantic import BaseModel, EmailStr, Field
from typing import Union


class UsersBase(BaseModel):
    """
    Pydantic model for users validation in the endpoint

    Attributes:
        - name: str
        - lastname1: str
        - lastname2: str | None
        - email: EmailStr
        - passwd: str
    """

    name: str = Field(min_length=1, max_length=70)
    lastname1: str = Field(min_length=1, max_length=70)
    lastname2: Union[str, None] = Field(default=None, max_length=70)
    email: EmailStr = Field(min_length=1, max_length=150)
    passwd: str = Field(min_length=8, max_length=50)
