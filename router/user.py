from db import db_user
from typing import List
from db.database import get_async_db
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio.session import AsyncSession
from schemas.schemas_user import UserModel, UserDisplay, UserPatchModel

router = APIRouter(prefix="/user", tags=["user"])


@router.post(
    "/create",
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
    deprecated=False,
    name='User_read_by_username',
    summary="Retrieve a user by their username",
    description="Fetch a specific user's details from the database using their unique username.",
    response_model=List[UserDisplay],
    status_code=status.HTTP_200_OK,
    response_description="User details retrieved successfully",
    responses={
        200: {
            "description": "SUCCESS - User found",
            "content": {
                "application/json": {
                    "example": [{"id": 1, "username": "diluc", "email": "diluc@example.com", 'timestamp': '2025-12-22T00:00:00'}]
                }
            }
        },
        404: {"description": "NOT FOUND - Username does not exist"}
    }
)
async def read_user_by_username(username: str, db: AsyncSession = Depends(get_async_db)):
    user = await db_user.read_user_by_username(username, db)
    return user


#--------------------------------------------------------------------------


@router.get(
    "/read_all_users",
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
async def update(id: int, request: UserModel, db: AsyncSession = Depends(get_async_db)):
    user = await db_user.update(id, request, db)
    return user


#--------------------------------------------------------------------------


@router.patch(
    "/patch",
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
async def patch(id: int, request: UserPatchModel, db: AsyncSession = Depends(get_async_db)):
    user = await db_user.patch(id, request, db)
    return user

#--------------------------------------------------------------------------

@router.delete(
    "/delete",
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
async def delete(id: int, db: AsyncSession = Depends(get_async_db)):
    await db_user.delete(id, db)
    return None