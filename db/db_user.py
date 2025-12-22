<<<<<<< Updated upstream
from fastapi import Depends, HTTPException, status
from db.database import get_async_db
from db.models import DbUser
from schemas.schemas_user import UserModel
from sqlalchemy.ext.asyncio.session import AsyncSession
from werkzeug.security import generate_password_hash
from sqlalchemy import exc, select, update as sql_update, delete as sql_delete


async def create(
        request: UserModel,
        db: AsyncSession = Depends(get_async_db)):
    try:
        new_user = DbUser(
            username=request.username,
            email=request.email,
            hashed_password=generate_password_hash(
                request.password,
                method="scrypt:32768:8:1",
                salt_length=16,
            )
        )
        db.add(new_user)
        await db.commit()
    except exc.SQLAlchemyError as e:
        await db.rollback()
        print(f"Database error during creation: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while saving changes to the database.",
        )
    return {"detail": "New User has been successfully added to the database."}
=======
import asyncio

from fastapi import HTTPException, status
from db.models import DbUser
from schemas.schemas_user import UserModel, UserPatchModel
from sqlalchemy.ext.asyncio.session import AsyncSession
from werkzeug.security import generate_password_hash
from sqlalchemy import select, update as sql_update, delete as sql_delete


async def create(request: UserModel, db: AsyncSession):

    new_hashed_password = await asyncio.to_thread(
        generate_password_hash,
        request.password,
        method="scrypt:32768:8:1",
        salt_length=16
    )

    new_user = DbUser(
        username=request.username,
        email=request.email,
        hashed_password=new_hashed_password,
    )
    db.add(new_user)
    await db.commit()
    return new_user
>>>>>>> Stashed changes


# --------------------------------------------------------------------------


<<<<<<< Updated upstream
async def read_user_by_username(
    username: str,
    db: AsyncSession = Depends(get_async_db)
):
=======
async def read_user_by_username(username: str, db: AsyncSession):
>>>>>>> Stashed changes
    query = select(DbUser).where(DbUser.username == username)
    result = await db.execute(query)
    user = result.scalars().all()
    return user

<<<<<<< Updated upstream
# --------------------------------------------------------------------------


async def read_all_users(
    db: AsyncSession = Depends(get_async_db)
):
=======

# --------------------------------------------------------------------------


async def read_all_users(db: AsyncSession):
>>>>>>> Stashed changes
    query = select(DbUser)
    result = await db.execute(query)
    user = result.scalars().all()
    return user


# --------------------------------------------------------------------------


<<<<<<< Updated upstream
async def update(
        id: int,
        request: UserModel,
        db: AsyncSession = Depends(get_async_db)):
    try:
        query = (
            sql_update(DbUser)
            .where(DbUser.id == id)
            .values(
                username=request.username,
                email=request.email,
                hashed_password=generate_password_hash(
                    request.password, 
                    method="scrypt:32768:8:1",
                    salt_length=16
                )
            )
        )

        await db.execute(query)
        await db.commit()
    except exc.SQLAlchemyError as e:
        await db.rollback()
        print(f"Database error during creation: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while saving changes to the database.",
        )
    return {"detail": "New User has been successfully added to the database."}
=======
async def update(id: int, request: UserModel, db: AsyncSession):

    new_hashed_password = await asyncio.to_thread(
        generate_password_hash,
        request.password,
        method="scrypt:32768:8:1",
        salt_length=16
    )

    query = (
        sql_update(DbUser)
        .where(DbUser.id == id)
        .values(
            username=request.username,
            email=request.email,
            hashed_password=new_hashed_password,
        )
        .returning(DbUser)
    )

    result = await db.execute(query)
    await db.commit()
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user
>>>>>>> Stashed changes


# --------------------------------------------------------------------------


<<<<<<< Updated upstream
async def delete(
        id: int,
        db: AsyncSession = Depends(get_async_db)):
    try:
        query = sql_delete(DbUser).where(DbUser.id == id)
        await db.execute(query)
        await db.commit()
    except exc.SQLAlchemyError as e:
        await db.rollback()
        print(f"Database error during creation: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while saving changes to the database.",
        )
=======
async def patch(id: int, request: UserPatchModel, db: AsyncSession):
    # Convert request to a dictionary, keeping only the fields the user actually sent
    update_data = request.model_dump(exclude_unset=True)

    if not update_data:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='The dict is empty')

    # If password is being updated, hash it before saving
    if "password" in update_data:
        new_password = update_data.pop("password")
        update_data["hashed_password"] = await asyncio.to_thread(
        generate_password_hash,
        new_password,
        method="scrypt:32768:8:1",
        salt_length=16
    )

    # Execute the update
    query = (
        sql_update(DbUser)
        .where(DbUser.id == id)
        .values(**update_data)  # Unpack the dict into the update query
        .returning(DbUser)
    )

    result = await db.execute(query)
    await db.commit()
    return result.scalar_one_or_none()


# --------------------------------------------------------------------------


async def delete(id: int, db: AsyncSession):
    query = sql_delete(DbUser).where(DbUser.id == id)
    await db.execute(query)
    await db.commit()
>>>>>>> Stashed changes
    return None
