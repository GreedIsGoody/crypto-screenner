import httpx 
from src.config import settings


class CoinGeckoClient:
    def __init__(self):
        self.base_url = "https://api.coingecko.com/api/v3"
        
        self.headers = {
            "accept": "application/json"
        }
    async def get_coin_prices(self, coin_ids: list[str]) -> dict:
        ids_param = ','.join(coin_ids)
        url = f"{self.base_url}/simple/price"
        
        params = {
            "ids" : ids_param,
            "vs_currencies": "usd"
        }
        async with httpx.AsyncClient(headers=self.headers) as client:
            try:
                response = await client.get(url, params=params, timeout=10.0)
                response.raise_for_status()
                return response.json()
            except httpx.HTTPError as e:
                print(f"Error in request to CoinGecko API : {e}")
                return {}
            
crypto_client = CoinGeckoClient()