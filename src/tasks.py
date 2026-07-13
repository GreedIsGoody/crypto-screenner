import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.database import async_session
from src.client import crypto_client
from src.models import Coin, CoinPrice


async def fetch_and_save_prices():
    while True:
        try:
            # 1. Открываем сессию к базе данных
            async with async_session() as session:
                # Получаем все монеты, которые мы хотим отслеживать
                result = await session.execute(select(Coin))
                coins = result.scalars().all()
                
                if not coins:
                    print("[Background Task] В базе данных пока нет монет для отслеживания.")
                else:
                    coin_ids = [coin.coingecko_id for coin in coins]
                    
                    prices_data = await crypto_client.get_coin_prices(coin_ids)
                    
                    for coin in coins:
                        coin_data = prices_data.get(coin.coingecko_id)
                        if coin_data and "usd" in coin_data:
                            new_price = CoinPrice(
                                coin_id=coin.id,
                                price_usd=coin_data["usd"]
                            )
                            session.add(new_price)
                    
                    await session.commit()
                    print(f"[Background Task] Success refreshing prices {len(coins)} coins.")
                    
        except Exception as e:
            print(f"[Background Task] Error in refreshing a prices: {e}")
            
        await asyncio.sleep(60)