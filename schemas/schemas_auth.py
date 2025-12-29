from pydantic import BaseModel, Field


class UserAuth(BaseModel):
    id: int = Field(
        Ellipsis,
        deprecated=False,
        description="The user's id.",
        json_schema_extra={"example": "1"},
    )
    username: str = Field(
        Ellipsis,
        deprecated=False,
        description="The user's name, aka: username.",
        json_schema_extra={"example": "janedoe"},
    )
    email: str = Field(
        Ellipsis,
        deprecated=False,
        description="The user's email.",
        json_schema_extra={"example": "janedoe@exemple.com"},
    )