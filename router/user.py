from schemas.schemas_user import UserModel, UserDisplay, UserPatchModel
from fastapi import APIRouter, Depends, HTTPException, status, Header
from sqlalchemy.ext.asyncio.session import AsyncSession
from schemas.schemas_auth import UserAuth
from auth.oauth2 import get_current_user
from db.database import get_async_db
from typing import List
from db import db_user
import os

router = APIRouter(prefix="/user", tags=["user"])

SECRET_KEY = os.getenv("SECRET_KEY")

async def verify_internal_token(x_internal_token: str = Header(Ellipsis)):
    if not SECRET_KEY:
            raise ValueError("CRITICAL: SECRET_KEY environment variable is required.")
    if x_internal_token != SECRET_KEY:
        raise HTTPException(status_code=403, detail="Access denied: Internal only")
    return x_internal_token

@router.post(
    "/create",
    include_in_schema=True,
    deprecated=False,
    name='User_Creation',
    summary="Create a new user",
    description="Registers a new user and saves their information into the PostgreSQL database.",
    response_model=UserDisplay,
    status_code=status.HTTP_201_CREATED,
    response_description="User created successfully",
    responses={
        201: {
            "description": "SUCCESS - User has been created",
            "content": {
                "application/json": {
                    "example": {
                        "id": 1,
                        "username": "janedoe",
                        "email": "janedoe@example.com"
                    }
                }
            }
        },
        409: {
            "description": "CONFLICT - Email or Username already exists"
        }
    }
)
async def create(request: UserModel, db: AsyncSession = Depends(get_async_db)):
    user = await db_user.create(request, db)
    return user


#--------------------------------------------------------------------------


@router.get(
    "/read_user_by_username",
    include_in_schema=False,
    deprecated=False,
    name='User_read_by_username',
    summary="Retrieve a user by their username",
    description="Fetch a specific user's details from the database using their unique username.",
    response_model=UserAuth,
    status_code=status.HTTP_200_OK,
    response_description="User details retrieved successfully",
    responses={
        200: {
            "description": "SUCCESS - User found",
            "content": {
                "application/json": {
                    "example": {"id": 1, "username": "diluc", "email": "diluc@example.com", 'timestamp': '2025-12-22T00:00:00'}
                }
            }
        },
        404: {"description": "NOT FOUND - Username does not exist"}
    }
)
async def read_user_by_username(username: str, db: AsyncSession = Depends(get_async_db), _ = Depends(verify_internal_token)):
    user = await db_user.read_user_by_username(username, db)
    return user


#--------------------------------------------------------------------------


@router.get(
    "/read_all_users",
    include_in_schema=True,
    deprecated=False,
    name='User_read_all',
    summary="Retrieve all registered users",
    description="Returns a complete list of all users stored in the PostgreSQL database.",
    response_model=List[UserDisplay],
    status_code=status.HTTP_200_OK,
    response_description="List of users retrieved successfully",
    responses={
        200: {
            "description": "SUCCESS - Users found",
            "content": {
                "application/json": {
                    "example": [{"id": 1, "username": "thrain", "email": "thrain@example.com"}]
                }
            }
        }
    }
)
async def read_all_users(db: AsyncSession = Depends(get_async_db)):
    user = await db_user.read_all_users(db)
    return user


#--------------------------------------------------------------------------


@router.put(
    "/update",
    include_in_schema=True,
    deprecated=False,
    name='User_update',
    summary="Update an existing user",
    description="Perform a full update of a user's information. All fields in the request body are required.",
    response_model=UserDisplay,
    status_code=status.HTTP_200_OK,
    response_description="User updated successfully",
    responses={
        200: {
            "description": "SUCCESS - User information overwritten",
            "content": {
                "application/json": {
                    "example": {"id": 1, "username": "new_username", "email": "new_email@example.com"}
                }
            }
        },
        404: {"description": "NOT FOUND - User ID not found"}
    }
)
async def update(request: UserModel, db: AsyncSession = Depends(get_async_db), current_user_id: int = Depends(get_current_user)):
    user = await db_user.update(request, db, current_user_id)
    return user


#--------------------------------------------------------------------------


@router.patch(
    "/patch",
    include_in_schema=True,
    deprecated=False,
    name='User_patch',
    summary="Partially update a user",
    description="Update specific fields of a user record without affecting the others. Ideal for changing just a password or email.",
    response_model=UserDisplay,
    status_code=status.HTTP_200_OK,
    response_description="User patched successfully",
    responses={
        200: {
            "description": "SUCCESS - User fields updated",
            "content": {
                "application/json": {
                    "example": {"detail": "User has been successfully patched in the database."}
                }
            }
        }
    }
)
async def patch(request: UserPatchModel, db: AsyncSession = Depends(get_async_db), current_user_id: int = Depends(get_current_user)):
    user = await db_user.patch(request, db, current_user_id)
    return user

#--------------------------------------------------------------------------

@router.delete(
    "/delete",
    include_in_schema=True,
    deprecated=False,
    name='User_delete',
    summary="Delete a user from the database",
    description="Permanently removes a user record from the PostgreSQL database using their unique ID.",
    response_model=None,
    status_code=status.HTTP_204_NO_CONTENT,
    response_description="User deleted successfully",
    responses={
        204: {
            "description": "SUCCESS - User has been deleted",
        },
        500: {
            "description": "SERVER ERROR - Database failure during deletion",
            "content": {
                "application/json": {
                    "example": {"detail": "Error - User could not be deleted from the database."}
                }
            }
        }
    }
)
async def delete(db: AsyncSession = Depends(get_async_db), current_user_id: int = Depends(get_current_user)):
    await db_user.delete(db, current_user_id)
    return None