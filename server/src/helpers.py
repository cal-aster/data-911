# Author:  Meryll Dindin
# Date:    November 04, 2020
# Project: CalAster

from src.scraper import *

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], #[os.getenv('CLIENT')],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

mng = Manager()

### Request tracking

@app.middleware("http")
async def tracker(
    request: Request,
    call_next
):

    ini = time.time()
    res = await call_next(request)

    try: org = str(request.headers['origin'])
    except: org = 'unknown'

    mng.sql.add(
    	'Trackings',
    	{
    		'endpoint': str(request.url.path),
    		'client': org,
            'port': request.client[1],
            'method': str(request.method),
            'status': int(res.status_code),
    		'completion': round(time.time() - ini, 6),
    		'timestamp': mng.timestamp()
    	}
    )

    return res