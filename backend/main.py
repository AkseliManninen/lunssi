from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from get_menu import get_menu
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

@app.get("/restaurant")
async def get_restaurant(name: Optional[str] = "bruuveri"):
    try:
        menu = get_menu(name)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return {
        "name": name.capitalize(),
        "lunchItems": [menu],
        "lunchPrice": "13,50€ (Noutopöytä) - 12,30€ (Kevytlounas)",
        "lunchTime": "10.30 - 13.30",
    }
