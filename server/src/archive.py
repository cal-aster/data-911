# Author:  Meryll Dindin
# Date:    November 04, 2020
# Project: CalAster
### To be processed

@app.post(
    "/type/spatial",
    tags=["records"],
    response_model=List[TypeRecord],
    summary="Returns list of spatial emergency type (includes class and possibly a description) records"
)
async def type_records(
    table: str = Body(..., title="Table name of city to describe"),
    start: str = Body(..., title="Start date request"),
    end: str = Body(None, title="End date request")
):
    """
        Returns a list of spatial emergency type records of
        calls for service from the corresponding table (city) that took place
        from the corresponding start date to end date.
    """
    return jsonable_encoder(mng.type_records(table, start, end))


@app.post(
    "/source/spatial",
    tags=["records"],
    response_model=List[SourceRecord],
    summary="Returns list of spatial call source records"
)
async def source_records(
    table: str = Body(..., title="Table name of city to describe"),
    start: str = Body(..., title="Start date request"),
    end: str = Body(None, title="End date request")
):
    """
        Returns a list of spatial call source records of
        calls for service from the corresponding table (city) that took place
        from the corresponding start date to end date.
    """
    return jsonable_encoder(mng.source_records(table, start, end))


@app.post(
    "/priorityassignment/spatial",
    tags=["records"],
    response_model=List[PriorityAssignmentRecord],
    summary="Returns list of spatial priority assignment records ('class', 'priority')"
)
async def priorityassignment_records(
    table: str = Body(..., title="Table name of city to describe"),
    start: str = Body(..., title="Start date request"),
    end: str = Body(None, title="End date request")
):
    """
        Returns a list of spatial priority assignment records of
        calls for service from the corresponding table (city) that took place
        from the corresponding start date to end date.
    """
    return jsonable_encoder(mng.priorityassignment_records(table, start, end))


@app.post(
    "/dispatch/spatial",
    tags=["records"],
    summary="Returns geojson of normalized spatial dispatch time records"
)
async def dispatch_records(
    table: str = Body(..., title="Table name of city to describe"),
    start: str = Body(..., title="Start date request"),
    end: str = Body(None, title="End date request")
):
    """
        Returns a list of spatial dispatch time records of
        calls for service from the corresponding table (city) that took place
        from the corresponding start date to end date.
    """
    return jsonable_encoder(mng.dispatch_records(table, start, end))


@app.post(
    "/arrival/spatial",
    tags=["records"],
    summary="Returns geojson of normalized spatial arrival time records (difference from arrival to call initiation)"
)
async def arrival_records(
    table: str = Body(..., title="Table name of city to describe"),
    start: str = Body(..., title="Start date request"),
    end: str = Body(None, title="End date request")
):
    """
        Returns a list of spatial response time records (time from call initiation to arrival) of
        calls for service from the corresponding table (city) that took place
        from the corresponding start date to end date.
    """
    return jsonable_encoder(mng.arrival_records(table, start, end))


@app.post(
    "/closed/spatial",
    tags=["records"],
    summary="Returns geojson of normalized spatial completion time records"
)
async def closed_records(
    table: str = Body(..., title="Table name of city to describe"),
    start: str = Body(..., title="Start date request"),
    end: str = Body(None, title="End date request")
):
    """
        Returns a list of spatial completion time records of
        calls for service from the corresponding table (city) that took place
        from the corresponding start date to end date.
    """
    return jsonable_encoder(mng.closed_records(table, start, end))

# Single endpoint statistics route

@app.post(
    "/stats/all",
    tags=["statistics"],
    summary="Returns all the stats"
)
async def all_stats(
    table: str = Body(..., title="Table name of city to describe"),
    start: str = Body(..., title="Start date request"),
    end: str = Body(None, title="End date request"),
):
    """
        Returns all the stats for calls for service from the corresponding table (city)
        that took place from the corresponding start date to end date.
    """
    warnings.simplefilter('ignore')
    return jsonable_encoder(mng.all_stats(table, start, end))

# District statistic chloropleth routes

@app.post(
    "/district/call_count",
    tags=["statistics"],
    summary="Returns geojson with the total call count for each district"
)
async def district_count(
    table: str = Body(..., title="Table name of city to describe"),
    start: str = Body(..., title="Start date request"),
    end: str = Body(None, title="End date request"),
):
    """
        Returns geojson with the total call count for each district for calls for service from the corresponding table (city)
        that took place from the corresponding start date to end date.
    """
    return jsonable_encoder(mng.district_count(table, start, end))


@app.post(
    "/district/emergency_count",
    tags=["statistics"],
    summary="Returns geojson with the count of emergency calls for each district"
)
async def district_emergency_count(
    table: str = Body(..., title="Table name of city to describe"),
    start: str = Body(..., title="Start date request"),
    end: str = Body(None, title="End date request"),
):
    """
        Returns geojson with the count of emergency calls for each district for calls for service from the corresponding table (city)
        that took place from the corresponding start date to end date.
    """
    return jsonable_encoder(mng.district_emergency_count(table, start, end))


@app.post(
    "/district/mean_dispatch",
    tags=["statistics"],
    summary="Returns geojson with the mean dispatch time (minutes) for each district"
)
async def district_mean_dispatch(
    table: str = Body(..., title="Table name of city to describe"),
    start: str = Body(..., title="Start date request"),
    end: str = Body(None, title="End date request"),
):
    """
        Returns geojson with the mean dispatch time (minutes) for each district for calls for service from the corresponding table (city)
        that took place from the corresponding start date to end date.
    """
    return jsonable_encoder(mng.district_mean_dispatch(table, start, end))


@app.post(
    "/district/mean_response_emergency",
    tags=["statistics"],
    summary="Returns geojson with the mean response time (seconds) for emergency calls for each district"
)
async def district_mean_response(
    table: str = Body(..., title="Table name of city to describe"),
    start: str = Body(..., title="Start date request"),
    end: str = Body(None, title="End date request"),
):
    """
        Returns geojson with the mean response time (seconds) for emergency calls for each district for calls for service from the corresponding table (city)
        that took place from the corresponding start date to end date.
    """
    return jsonable_encoder(mng.district_mean_response(table, start, end))


@app.post(
    "/district/hourly_dispatch",
    tags=["statistics"],
    summary="Returns geojson with the mean number of calls dispatched hourly for each district"
)
async def district_hourly_dispatch(
    table: str = Body(..., title="Table name of city to describe"),
    start: str = Body(..., title="Start date request"),
    end: str = Body(None, title="End date request"),
):
    """
        Returns geojson with the mean number of calls dispatched hourly for each district for calls for service from the corresponding table (city)
        that took place from the corresponding start date to end date.
    """
    return jsonable_encoder(mng.district_hourly_dispatch(table, start, end))


@app.post(
    "/district/mean_overlap",
    tags=["statistics"],
    summary="Returns geojson with the mean number of calls that overlap for each district"
)
async def district_mean_overlap(
    table: str = Body(..., title="Table name of city to describe"),
    start: str = Body(..., title="Start date request"),
    end: str = Body(None, title="End date request"),
):
    """
        Returns geojson with the mean number of calls that overlap for each district for calls for service from the corresponding table (city)
        that took place from the corresponding start date to end date.
    """
    return jsonable_encoder(mng.district_mean_overlap(table, start, end))
