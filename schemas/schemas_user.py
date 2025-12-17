from pydantic import BaseModel, Field


class UserModel(BaseModel):
    username: str = Field(
        Ellipsis,
        min_length=2,
        max_length=40,
        deprecated=False,
    )
    email: str = Field(
        Ellipsis,
        min_length=5,
        max_length=60,
        deprecated=False,
    )
    password: str = Field(
        Ellipsis,
        min_length=1,
        max_length=70,
        deprecated=False,
    )
    
#--------------------------------------------------------------------------

class UserDisplay(BaseModel):
    id: int
    username: str
    email: str

    class ConfigDict:
        from_attributes = True
