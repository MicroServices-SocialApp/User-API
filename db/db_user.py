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


# --------------------------------------------------------------------------


async def read_user_by_username(
    username: str,
    db: AsyncSession = Depends(get_async_db)
):
    query = select(DbUser).where(DbUser.username == username)
    result = await db.execute(query)
    user = result.scalars().all()
    return user

# --------------------------------------------------------------------------


async def read_all_users(
    db: AsyncSession = Depends(get_async_db)
):
    query = select(DbUser)
    result = await db.execute(query)
    user = result.scalars().all()
    return user


# --------------------------------------------------------------------------


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


# --------------------------------------------------------------------------


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
    return None
