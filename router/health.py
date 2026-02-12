from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio.session import AsyncSession
from db.database import get_async_db
from sqlalchemy import text

router = APIRouter(tags=["system"])

@router.get("/health", tags=["system"])
async def health_check(db: AsyncSession = Depends(get_async_db)) -> dict[str, str]:
    try:
        # Execute a trivial query to confirm DB connectivity
        await db.execute(text("SELECT 1"))
        return {"status": "healthy", "database": "connected"}
    except Exception as e:
        print(f"HEALTH CHECK FAILURE: {e}")
        # If the DB is down, return a 503 so K8s knows the pod is failing
        raise HTTPException(
            status_code=503, 
            detail=f"Database connection failed: {str(e)}"
        )