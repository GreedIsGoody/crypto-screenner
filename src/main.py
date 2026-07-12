from fastapi import FastAPI


app = FastAPI(title='Crypto Screener API')

@app.get('/'):
async def root():
    return {"status": "ok", "message": "Crypto Screener is running"}