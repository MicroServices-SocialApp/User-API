from typing import List
from fastapi import APIRouter, Depends, status
from db import db_user
from sqlalchemy.ext.asyncio.session import AsyncSession
from db.database import get_async_db
from schemas.schemas_user import UserModel, UserDisplay

router = APIRouter(prefix="/user", tags=["user"])


@router.post(
    "/create",
    deprecated=False,
    name='User_Creation',
    summary="une phrase qui resume la fonction.",
    description="une decription longue et precise?",
    response_model=None,
    status_code=status.HTTP_201_CREATED,
    response_description="Succes de la reponse",
    responses={
        201: {
            "description": "SUCCESS - User has been created",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "New User has been succefully added to the database."
                    }
                }
            }
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
    summary="une phrase qui resume la fonction.",
    description="une decription longue et precise?",
    response_model=List[UserDisplay],
    status_code=status.HTTP_200_OK,
    response_description="Succes de la reponse",
    responses={
        200: {
            "description": "SUCCESS - User has been Found",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "User has been succefully found in the database."
                    }
                }
            }
        }
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
    summary="une phrase qui resume la fonction.",
    description="une decription longue et precise?",
    response_model=List[UserDisplay],
    status_code=status.HTTP_200_OK,
    response_description="Succes de la reponse",
    responses={
        200: {
            "description": "SUCCESS - User has been Found",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Users has been succefully found in the database."
                    }
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
    summary="une phrase qui resume la fonction.",
    description="une decription longue et precise?",
    response_model=None,
    status_code=status.HTTP_200_OK,
    response_description="Succes de la reponse",
    responses={
        200: {
            "description": "SUCCESS - User has been Updated",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "User has been succefully updated to the database."
                    }
                }
            }
        }
    }
)
async def update(id: int, request: UserModel, db: AsyncSession = Depends(get_async_db)):
    user = await db_user.update(id, request, db)
    return user

#--------------------------------------------------------------------------

@router.delete(
    "/delete",
    deprecated=False,
    name='User_delete',
    summary="une phrase qui resume la fonction.",
    description="une decription longue et precise?",
    response_model=None,
    status_code=status.HTTP_204_NO_CONTENT,
    response_description="Succes de la reponse",
    responses={
        204: {
            "description": "SUCCESS - User has been delete",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "User has been succefully delete from the database."
                    }
                }
            }
        },
        500: {
            "description": "SQLAlchemyError - User FAILED to be deleted!",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Error - User has FAILED to be delete from the database."
                    }
                }
            }
        }
    }
)
async def delete(id: int, db: AsyncSession = Depends(get_async_db)):
    await db_user.delete(id, db)
    return None