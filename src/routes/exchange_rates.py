from datetime  import datetime
from pydantic import BaseModel, ConfigDict
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select 
from src.database import get_db
from src.models import ExchangeRate


router = APIRouter(prefix="/exchange-rates", tags=["Exchange Rates"])


class ExchangeRateResponse(BaseModel):
    id: int
    currency_code: str
    rate_to_usd: float 
    update_at: datetime
    
    model_config = ConfigDict(from_attributes=True)
    
    
async def db_get_all_rates(db: AsyncSession):
    query = select(ExchangeRate)
    result = await db.execute(query)
    return result.scalars().all()

async def db_get_rate_by_code(db:AsyncSession, currency_code: str):
    query = select(ExchangeRate).where(
        ExchangeRate.currency_code  == currency_code.upper()
    )
    result = await db.execute(query)
    return result.scalar_one_or_none()


@router.get("/", response_model=list[ExchangeRateResponse])
async def read_all_rates(db: AsyncSession = Depends(get_db)):
    rates = await db_get_all_rates(db)
    return rates

@router.get("/{currency_code}", response_model=ExchangeRateResponse)
async def read_rate_by_code(
    currency_code:  str, db:AsyncSession = Depends(get_db)
):
    rate = await db_get_rate_by_code(db, currency_code)
    if not rate:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Course of this crypto was not found"
        )
    return rate