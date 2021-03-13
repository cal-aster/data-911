# Author:  Meryll Dindin
# Date:    November 04, 2020
# Project: CalAster

from src.imports import FastAPI, CORSMiddleware, Request, time
from services import sql_executor, timestamps

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

### Request tracking


@app.middleware("http")
async def tracker(request: Request, call_next):

    reception_time = time.time()
    request_result = await call_next(request)

    try:
        origin = str(request.headers["origin"])
    except:
        origin = "unknown"

    sql_executor.add(
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
