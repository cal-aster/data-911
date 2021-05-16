import os

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

dotenv_path = os.path.join(".devops", ".env.development")
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path=dotenv_path)

from src.routers import base, rds

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)

app.include_router(base.router, prefix="", tags=["Basic"])
app.include_router(rds.router, prefix="/rds", tags=["RDS"])
