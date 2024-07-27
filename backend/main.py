from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from get_menu import get_menu

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
async def get_restaurant():
    menu = get_menu()
    return {
        "name": "Bruuveri",
        "lunchItems": [menu],
        "lunchPrice": "13,50€ (Noutopöytä) - 12,30€ (Kevytlounas)",
        "lunchTime": "10.30 - 13.30",
    }