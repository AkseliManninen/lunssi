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
        "lunchPrice": 12,
        "lunchTime": "12:00 PM - 2:00 PM",
    }