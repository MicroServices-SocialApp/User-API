<<<<<<< Updated upstream
from pydantic import BaseModel, Field
=======
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, Field, field_serializer
>>>>>>> Stashed changes


class UserModel(BaseModel):
    username: str = Field(
        Ellipsis,
        min_length=2,
        max_length=40,
        deprecated=False,
<<<<<<< Updated upstream
    )
    email: str = Field(
=======
        description="New username.",
        json_schema_extra={"example": "janedoe"}
    )
    email: EmailStr = Field(
>>>>>>> Stashed changes
        Ellipsis,
        min_length=5,
        max_length=60,
        deprecated=False,
<<<<<<< Updated upstream
=======
        description="New email.",
        json_schema_extra={"example": "email@example.com"}
>>>>>>> Stashed changes
    )
    password: str = Field(
        Ellipsis,
        min_length=1,
        max_length=70,
        deprecated=False,
<<<<<<< Updated upstream
=======
        description="New password. Will be re-hashed.",
        json_schema_extra={"example": "SecurePassword456!"}
>>>>>>> Stashed changes
    )
    
#--------------------------------------------------------------------------

<<<<<<< Updated upstream
=======
class UserPatchModel(BaseModel):
    username: Optional[str] = Field(
        default=None,
        min_length=2,
        max_length=40,
        deprecated=False,
        description="New username if a change is desired.",
        json_schema_extra={"example": "new_janedoe"}
    )
    email: Optional[EmailStr] = Field(
        default=None,
        min_length=5,
        max_length=60,
        deprecated=False,
        description="New email address if a change is desired.",
        json_schema_extra={"example": "new.email@example.com"}
    )
    password: Optional[str] = Field(
        default=None,
        min_length=8,
        max_length=70,
        deprecated=False,
        description="New password if a change is desired. Will be re-hashed.",
        json_schema_extra={"example": "NewSecurePassword456!"}
    )

#--------------------------------------------------------------------------

>>>>>>> Stashed changes
class UserDisplay(BaseModel):
    id: int
    username: str
    email: str
<<<<<<< Updated upstream

    class ConfigDict:
        from_attributes = True
=======
    timestamp: datetime
    class ConfigDict:
        from_attributes = True

    @field_serializer('timestamp')
    def format_timestamp(self, dt: datetime) -> str:
        # .strftime converts the datetime object to your specific string format
        return dt.strftime('%Y-%m-%dT%H:%M')
>>>>>>> Stashed changes
