from fastapi import APIRouter, Response, status
from fastapi.encoders import jsonable_encoder
from services import sql_handler, timestamps

router = APIRouter()


@router.get(
    "/health",
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
    summary="Depict backend performances",
)
async def performances():
    results = dict()
    one_day = timestamps.now() - 24 * 3600
    seven_days = timestamps.now() - 7 * 24 * 3600
    four_weeks = timestamps.now() - 28 * 24 * 3600

    for (acronym, offset) in [
        ("t1d", one_day),
        ("t7d", seven_days),
        ("t28", four_weeks),
    ]:
        results.update(
            sql_handler.get_unique(
                f"SELECT MAX(completion) as top_{acronym}, \
                    MIN(completion) as min_{acronym}, \
                    AVG(completion) as avg_{acronym} \
                FROM Trackings WHERE timestamp >= ?",
                (offset,),
            )
        )

    return jsonable_encoder(results)
