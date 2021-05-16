from typing import List, Union

from fastapi import APIRouter, Body, Depends, HTTPException, Query, Response
from fastapi.encoders import jsonable_encoder
from src.models.auth import UserModel
from src.services import authentication, rds_handler

router = APIRouter()


@router.post(
    "/get",
    summary="Fetch records given a query",
)
async def get(
    query: str = Body(..., embed=True, title="MySQL Query"),
    unique: bool = Query(False, title="Whether to fetch a unique value"),
    _: UserModel = Depends(authentication.verify()),
):
    """
    Returns the results of the query
    """
    try:
        if unique:
            res = rds_handler.get_unique(query)
        else:
            res = rds_handler.get(query)
        return jsonable_encoder(res)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post(
    "/run",
    summary="Executes one or multiple queries",
)
async def run(
    query: Union[str, List[str]] = Body(..., embed=True, title="MySQL Query"),
    _: UserModel = Depends(authentication.verify()),
):
    """
    Returns the results of the query
    """
    try:
        if isinstance(query, str):
            rds_handler.run(query)
        else:
            rds_handler.run_batch(query)
        return Response(status_code=200)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post(
    "/add",
    summary="Adds one or multiple items to a given table",
)
async def add(
    table: str = Body(..., embed=True, title="Name of the table"),
    item: Union[dict, List[dict]] = Body(..., embed=True, title="List of items to add"),
    _: UserModel = Depends(authentication.verify()),
):
    """
    Returns the results of the query
    """
    try:
        if isinstance(item, dict):
            rds_handler.add(table, item)
        else:
            rds_handler.add_batch(table, item)
        return Response(status_code=200)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/describe", summary="Returns the list of tables", response_model=dict)
async def tables(_: UserModel = Depends(authentication.verify())):
    """
    Returns the schemas of all the available tables
    """
    return jsonable_encoder(rds_handler.describe())


@router.post(
    "/table",
    summary="Creates a new table",
)
async def table_create(
    table: str = Body(..., embed=True, title="Name of the table"),
    schema: dict = Body(..., embed=True, title="Schema of the table"),
    _: UserModel = Depends(authentication.verify()),
):
    """
    Creates a new table
    """
    try:
        rds_handler.create_table(table, schema)
        return Response(status_code=200)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete(
    "/table",
    summary="Deletes a table",
)
async def table_delete(
    table: str = Body(..., embed=True, title="Name of the table"),
    _: UserModel = Depends(authentication.verify()),
):
    """
    Deletes a table
    """
    try:
        rds_handler.delete_table(table)
        return Response(status_code=200)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
