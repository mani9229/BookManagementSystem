#   main.py (FastAPI)
from fastapi import FastAPI
from app.api import router  # Import the main router
from app.database import create_db_and_tables
import asyncio

app = FastAPI()
app.include_router(router)  # Include the main router

@app.on_event("startup")
async def startup_event():
    await create_db_and_tables()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
