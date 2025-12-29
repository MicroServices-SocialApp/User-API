from pydantic import BaseModel, Field


class UserAuth(BaseModel):
    id: int = Field(
        Ellipsis,
        deprecated=False,
        description="The user's id.",
        json_schema_extra={"example": "1"},
    )
    hashed_password: str = Field(
        Ellipsis,
        deprecated=False,
        description="The user's crypted password.",
        json_schema_extra={"example": "486hdfn64bv6r48w6d8b4b,;:!:;,&é'(-è_çà)="},
    )