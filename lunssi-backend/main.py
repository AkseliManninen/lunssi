from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

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
    return {
        "name": "Bruuveri",
        "lunchItems": ["Pizza", "Burger", "Salad"],
        "lunchPrice": 15.99,
        "lunchTime": "12:00 PM - 2:00 PM",
    }