from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
import os
from database import db

app = FastAPI(title="PromoGen MVP Backend", version="0.1.0")

# CORS for local dev + hosted preview
origins = [
    "*",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {"message": "PromoGen backend is running"}


@app.get("/test")
def test():
    database_url = os.getenv("DATABASE_URL", "")
    database_name = os.getenv("DATABASE_NAME", "")
    try:
        collections = db.list_collection_names() if db is not None else []
        status = "connected" if db is not None else "not_configured"
    except Exception as e:
        collections = []
        status = f"error: {e}" 
    return {
        "backend": "ok",
        "database": "mongodb",
        "database_url": database_url[:6] + "***" if database_url else "",
        "database_name": database_name,
        "connection_status": status,
        "collections": collections,
    }

# Simple in-memory presets (non-persistent, just for demo). In a real app use MongoDB.
PRESETS = [
    {
        "id": "orbit",
        "name": "Orbit",
        "description": "Slow 360° orbit around the device",
        "duration": 3,
    },
    {
        "id": "dolly",
        "name": "Dolly",
        "description": "Push-in and pull-out dolly move",
        "duration": 3,
    },
    {
        "id": "rotate",
        "name": "Rotate",
        "description": "Device rotates in place",
        "duration": 3,
    },
]


@app.get("/presets")
def get_presets():
    return {"presets": PRESETS}
