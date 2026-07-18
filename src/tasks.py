import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy import select
from src.database import async_session
from src.client import crypto_client
from src.models import Coin, CoinPrice
from src.models import  ExchangeRate

async def fetch_and_save_prices():
    while True:
        try:
            
            async with async_session() as session:
               
                result = await session.execute(select(Coin))
                coins = result.scalars().all()
                
                if not coins:
                    print("[Background Task] In database don`t have a token")
                else:
                    coin_ids = [coin.coingecko_id for coin in coins]
                    
                    prices_data = await crypto_client.get_coin_prices(coin_ids)
                    print(prices_data)
                    for coin in coins:
                        coin_data = prices_data.get(coin.coingecko_id)
                        if coin_data and "usd" in coin_data:
                            price_usd = float(coin_data["usd"])
                            new_price = CoinPrice(
                                coin_id=coin.id,
                                price_usd=coin_data["usd"]
                            )
                            session.add(new_price)
                            
                            currency_code = coin.coingecko_id.upper()
                            
                            stmt = (
                                insert(ExchangeRate)
                                .values(
                                    currency_code=currency_code,
                                    rate_to_usd = price_usd
                                )
                                .on_conflict_do_update(
                                    index_elements = [ExchangeRate.currency_code],
                                    set_={"rate_to_usd" : price_usd}
                                )
                            )
                            await session.execute(stmt)
                    
                    await session.commit()
                    print(f"[Background Task] Success refreshing prices {len(coins)} coins.")
                    
        except Exception as e:
            print(f"[Background Task] Error in refreshing a prices: {e}")
            
        await asyncio.sleep(60)