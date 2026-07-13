from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select 
from pydantic import BaseModel
from datetime import datetime 
from typing import List

from src.database import get_db
from src.models import Coin, CoinPrice

router = APIRouter(
    prefix="/prices",
    tags=["Prices"]
)

class PriceHistoryResponse(BaseModel):
    price_usd: float 
    timestamp: datetime
    
    class Config:
        from_attributes = True
        

@router.get("/{ticker}", response_model=List[PriceHistoryResponse])
async def get_price_history(ticker: str, db:AsyncSession = Depends(get_db)):
    coin_query = select(Coin).where(Coin.ticker == ticker.lower())
    coin_result = await db.execute(coin_query)
    coin = coin_result.scalar_one_or_none()
    
    if not coin:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Coin was not found"
        )
        
    price_query = (
        select(CoinPrice)
        .where(CoinPrice.coin_id == coin.id)
        .order_by(CoinPrice.timestamp.desc())
    )
    prices_result = await db.execute(price_query)
    prices = prices_result.scalars().all()
    
    return prices
    