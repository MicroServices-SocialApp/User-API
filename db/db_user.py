from sqlalchemy import select, update as sql_update, delete as sql_delete
from schemas.schemas_user import UserModel, UserPatchModel
from sqlalchemy.ext.asyncio.session import AsyncSession
from werkzeug.security import generate_password_hash
from fastapi import HTTPException, status
from db.models import DbUser
import asyncio


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


# --------------------------------------------------------------------------


async def read_user_by_user_id(id: int, db: AsyncSession):

    query = select(DbUser).where(DbUser.id == id)
    result = await db.execute(query)
    user = result.scalar_one_or_none()
    return user


# --------------------------------------------------------------------------


async def read_user_by_username(username: str, db: AsyncSession):

    query = select(DbUser).where(DbUser.username == username)
    result = await db.execute(query)
    user = result.scalar_one_or_none()
    return user


# --------------------------------------------------------------------------


async def read_all_users(db: AsyncSession):

    query = select(DbUser)
    result = await db.execute(query)
    user = result.scalars().all()
    return user


# --------------------------------------------------------------------------


async def update(request: UserModel, db: AsyncSession, current_user_id: int):

    new_hashed_password = await asyncio.to_thread(
        generate_password_hash,
        request.password,
        method="scrypt:32768:8:1",
        salt_length=16
    )

    query = (
        sql_update(DbUser)
        .where(DbUser.id == current_user_id)
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


# --------------------------------------------------------------------------


async def patch(request: UserPatchModel, db: AsyncSession, current_user_id: int):
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
        .where(DbUser.id == current_user_id)
        .values(**update_data)  # Unpack the dict into the update query
        .returning(DbUser)
    )

    result = await db.execute(query)
    await db.commit()
    return result.scalar_one_or_none()


# --------------------------------------------------------------------------


async def delete(db: AsyncSession, current_user_id: int):
    query = sql_delete(DbUser).where(DbUser.id == current_user_id)
    await db.execute(query)
    await db.commit()
    return None
  
