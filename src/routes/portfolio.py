from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select 
from pydantic import BaseModel
from datetime import datetime 
from typing import List

from src.database import get_db 
from src.models import Coin, CoinPrice, Transaction

router = APIRouter(prefix="/portfolio", tags=["Portfolio"])

class TransactionsCreate(BaseModel):
    ticker: str
    amount: float
    purchase_price_usd: float
    
class TransactionResponse(BaseModel):
    id: int
    ticker: str
    amount: float 
    purchase_price_usd: float 
    created_at: datetime
    
    class Config:
        from_attributes = True
        
class CoinStatus(BaseModel):
    total_cost: float
    current_value: float 
    total_profit: float 
    current_price:float 
    current_value: float
    profit_usd: float 
    profit_percent: float 
    
    
class PortfolioStatusResponse(BaseModel):
    total_cost: float 
    current_value: float 
    total_profit_percent: float 
    assets: List[CoinStatus]

@router.post("/transactions", response_model=TransactionResponse, status_code=status.HTTP_201_CREATED)
async def add_transaction(data: TransactionsCreate, db:AsyncSession = Depends(get_db)):
    
    stmt = select(Coin).where(Coin.ticker == data.ticker.lower())
    result = await db.execute(stmt)
    coin = result.scalar_one_or_none()
    
    if not coin: 
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Coin with ticker '{data.ticker}' is not tracked. Add it first via POST /coins/"
        )
        
    new_transaction = Transaction (
        coin_id = coin.id,
        ticker=coin.ticker,
        amount=data.amount,
        purchase_price_usd = data.purchase_price_usd
    )
    
    db.add(new_transaction)
    await db.commit()
    await db.refresh(new_transaction)
    return new_transaction

@router.get("/transactions", response_model=List[TransactionResponse])
async def get_transactions(db: AsyncSession = Depends(get_db)):
    stmt = select(Transaction).order_by(Transaction.created_at.desc())
    result = await db.execute(stmt)
    
    return result.scalars().all()


@router.get("/status", response_model=PortfolioStatusResponse)
async def get_portfolio_status(db: AsyncSession = Depends(get_db)):
    
    tx_stmt = select(Transaction)
    tx_result = await db.execute(tx_stmt)
    transactions = tx_result.scalars().all()
    
    if not transactions:
        
        return {
            "total_cost": 0.0,
            "current_value": 0.0,
            "total_profit_usd": 0.0,
            "total_profit_percent": 0.0,
            "assets": []
        }
    
    
    portfolio = {}
    for tx in transactions:
        ticker = tx.ticker
        if ticker not in portfolio:
            portfolio[ticker] = {"amount": 0.0, "total_cost": 0.0}
        
        portfolio[ticker]["amount"] += tx.amount
        portfolio[ticker]["total_cost"] += tx.amount * tx.purchase_price_usd

    
    assets = []
    total_cost_sum = 0.0
    total_current_value_sum = 0.0
    
    for ticker, info in portfolio.items():
        if info["amount"] <= 0:
            continue
        
       
        price_stmt = (
            select(CoinPrice)
            .join(Coin)
            .where(Coin.ticker == ticker)
            .order_by(CoinPrice.timestamp.desc())
            .limit(1)
        )
        price_result = await db.execute(price_stmt)
        latest_price_obj = price_result.scalar_one_or_none()
        
        # Безопасно приводим к float
        current_price = float(latest_price_obj.price_usd) if latest_price_obj else (info["total_cost"] / info["amount"])
        
        coin_current_value = info["amount"] * current_price
        coin_profit_usd = coin_current_value - info["total_cost"]
        coin_profit_percent = (coin_profit_usd / info["total_cost"] * 100) if info["total_cost"] > 0 else 0.0
        
        total_cost_sum += info["total_cost"]
        total_current_value_sum += coin_current_value
        
        
        assets.append({
            "ticker": ticker,
            "amount": info["amount"],
            "total_cost": round(info["total_cost"], 2),
            "current_price": round(current_price, 4),
            "current_value": round(coin_current_value, 2),
            "profit_usd": round(coin_profit_usd, 2),
            "profit_percent": round(coin_profit_percent, 2)
        })
        
    total_profit_usd = total_current_value_sum - total_cost_sum
    total_profit_percent = (total_profit_usd / total_cost_sum * 100) if total_cost_sum > 0 else 0.0
    
    return {
        "total_cost": round(total_cost_sum, 2),
        "current_value": round(total_current_value_sum, 2),
        "total_profit_usd": round(total_profit_usd, 2),
        "total_profit_percent": round(total_profit_percent, 2),
        "assets": assets
    }