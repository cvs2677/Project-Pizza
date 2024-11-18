from fastapi import FastAPI
from app.api import auth, orders, users
from app.db.base import Base
from app.db.session import engine



Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Pizza Delivery API",
    description="API for pizza delivery service",
    version="1.0.0"
)

@app.get("/")
async def root():
    return {"message": "Welcome to the Pizza Delivery API"}

app.include_router(auth.router)
app.include_router(orders.router)
app.include_router(users.router)
