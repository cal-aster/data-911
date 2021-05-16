import os
import time

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.requests import Request

if os.path.exists(".devops/.env.development"):
    load_dotenv(dotenv_path=".devops/.env.development")

from routers import cities, general, spatial, temporal
from services import sql_handler, timestamps

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(cities.router, prefix="/city", tags=["city"])
app.include_router(general.router, tags=["base"])
app.include_router(spatial.router, prefix="/spatial", tags=["spatial"])
app.include_router(temporal.router, prefix="/temporal", tags=["temporal"])


@app.middleware("http")
async def tracker(request: Request, call_next):

    reception_time = time.time()
    request_result = await call_next(request)
    origin = request.headers.get("origin")

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
