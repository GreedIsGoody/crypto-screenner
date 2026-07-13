from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import or_
from pydantic import BaseModel, Field
from typing import List


from src.models import Coin
from src.database import get_db

router = APIRouter(
    prefix="/coins",
    tags=["Coins"]
)

class CoinCreate(BaseModel):
    coingecko_id: str = Field(..., max_length=50, example="bitcoin")
    ticker: str = Field(..., max_length=10, example="btc")
    name: str = Field(..., max_length=50, example="Bitcoin")
    
class CoinResponse(CoinCreate):
    id: int
    
    class Config:
        from_attributes = True
        

@router.post('/', response_model=CoinResponse, status_code=status.HTTP_201_CREATED)
async def add_coin(coin_data: CoinCreate, db:AsyncSession = Depends(get_db)):
    
    query = select(Coin).where(or_(Coin.coingecko_id == coin_data.coingecko_id, Coin.ticker == coin_data.ticker.lower()))
    result = await db.execute(query)
    existing_coin = result.scalar_one_or_none()
    
    if existing_coin:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Coin with coingecko_id already tracking"
        )
        
    new_coin = Coin(
        coingecko_id=coin_data.coingecko_id.lower(),
        ticker= coin_data.ticker.lower(),
        name= coin_data.name
    )
    db.add(new_coin)
    await db.commit()
    await db.refresh(new_coin)
    return new_coin

@router.get("/", response_model=List[CoinResponse])
async def get_coins(db: AsyncSession = Depends(get_db)):
    
    result = await db.execute(select(Coin))
    coins = result.scalars().all()
    return coins


@router.delete("/{coin_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_coin(coin_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Coin).where(Coin.id == coin_id))
    coin = result.scalar_one_or_none()
    
    if not coin:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Coin is not found"
        )
        
    await db.delete(coin)
    await db.commit()
    return None