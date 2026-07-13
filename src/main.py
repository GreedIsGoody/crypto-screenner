import asyncio
from fastapi import FastAPI
from contextlib import asynccontextmanager
from src.database import engine, Base
from src.tasks import fetch_and_save_prices
from src.routes.coins import router as coins_router
from src.routes.prices import router as prices_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        
        
    bg_task = asyncio.create_task(fetch_and_save_prices())
    yield
    
    bg_task.cancel()
    pass

app = FastAPI(title='Crypto Screener API', lifespan=lifespan)


app.include_router(coins_router)
app.include_router(prices_router)

@app.get('/')
async def root():
    return {"status": "ok", "message": "Crypto Screener is running"}