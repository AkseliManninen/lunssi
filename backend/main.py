from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from get_lunch_info import get_lunch_info
from typing import Optional

app = FastAPI()

# Add CORS middleware to allow requests from the frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def hello_fly():
    return 'hello from fly.io'

@app.get("/restaurant")
async def get_restaurant(name: Optional[str] = "bruuveri"):
    try:
        menu, lunch_price, lunch_available  = get_lunch_info(name)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return {
        "name": name.capitalize(),
        "lunchItems": [menu],
        "lunchPrice": lunch_price,
        "lunchTime": lunch_available,
    }
