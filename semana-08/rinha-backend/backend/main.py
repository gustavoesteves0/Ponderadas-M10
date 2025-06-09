from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import transaction, user
from database.postgres import database, metadata, DATABASE_URL
from sqlalchemy.ext.asyncio import create_async_engine
import os
import socket

instance_name = os.getenv("INSTANCE_NAME", "unknown")
app = FastAPI()

app.include_router(user.router)
app.include_router(transaction.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

engine = create_async_engine(DATABASE_URL, echo=True)

@app.get("/")
async def root():
    return {"message": "working"}

@app.on_event("startup")
async def startup():
    await database.connect()
    async with engine.begin() as conn:
        await conn.run_sync(metadata.create_all)

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

@app.get("/ping")
async def ping():
    return {
        "message": f"pong from {instance_name}",
        "host": instance_name,  # Adicionando para compatibilidade com o teste
        "instance": instance_name
    }