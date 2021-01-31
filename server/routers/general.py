# Author:  Meryll Dindin
# Date:    November 04, 2020
# Project: CalAster

from src.helpers import *

router = APIRouter()

@router.get(
    "/health",
    tags=["status"],
    response_model=str,
    summary="Simple route for health check.",
)
async def health():
    """
        Returns simple response for health check.
    """
    return Response(status_code=status.HTTP_200_OK)

@router.get(
    "/performances",
    tags=["performances"],
    summary="Depict backend performances",
)
async def performances():

    res = dict()
    t1d = mng.timestamp() - 24*3600
    t7d = mng.timestamp() - 7*24*3600
    t28 = mng.timestamp() - 28*24*3600

    for (suf, tme) in [("t1d", t1d), ("t7d", t7d), ("t28", t28)]:
        qry = f"SELECT MAX(completion) as top_{suf}, \
                    MIN(completion) as min_{suf}, \
                    AVG(completion) as avg_{suf} \
                FROM Trackings WHERE timestamp >= {tme}"
        res.update(mng.sql.unique(qry))

    return jsonable_encoder(res)