# Author:  Meryll Dindin
# Date:    November 04, 2020
# Project: CalAster

import os
import time

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.requests import Request

from services import sql_handler, timestamps

if os.path.exists(".devops/.env.development"):
    load_dotenv(dotenv_path=".devops/.env.development")

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def tracker(request: Request, call_next):

    reception_time = time.time()
    request_result = await call_next(request)

    try:
        origin = str(request.headers["origin"])
    except:
        origin = "unknown"

    sql_handler.add(
        "Trackings",
        {
            "endpoint": str(request.url.path),
            "client": origin,
            "port": request.client[1],
            "method": str(request.method),
            "status": int(request_result.status_code),
            "completion": round(time.time() - reception_time, 6),
            "timestamp": timestamps.now(),
        },
    )

    return request_result
