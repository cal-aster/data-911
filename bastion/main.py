# Author:  Meryll Dindin
# Date:    November 04, 2020
# Project: CalAster

from src.helpers import *

### General application routes

@app.get(
    "/health",
    tags=["default"],
    response_model=str,
    summary="Simple route for health check.",
)
async def health():
    """
        Returns simple response for health check.
    """
    return "online"

@app.post(
    "/auth",
    tags=["default"],
    response_model=str,
    summary="Generate a JWT from a login attempt",
)
async def login(
    username: str = Body(..., embed=True, title="User id"),
    password: str = Body(..., embed=True, title="User password")
):
    """
        Standard authentication login. Returns JWT with encoded user's data.
    """
    usr: User = app_jwt.authenticate(username, password)

    if usr is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return app_jwt.create_token({"identity": usr.id})

# RDS routines

@app.post(
    "/rds/get",
    tags=["RDS"],
    summary="Returns the list of accessible factories",
)
async def rds_get(
    query: str = Body(..., embed=True, title="MySQL Query"),
    unique: bool = Query(False, title="Whether to fetch a unique value"),
    current_user: User = Depends(app_jwt.verify())
):
    """
        Returns the results of the query
    """
    if unique: res = app_sql.unique(query)
    else: res = app_sql.get(query)
    return jsonable_encoder(res)

@app.post(
    "/rds/run",
    tags=["RDS"],
    summary="Executes one or multiple queries",
)
async def rds_run(
    query: Union[str, List[str]] = Body(..., embed=True, title="MySQL Query"),
    current_user: User = Depends(app_jwt.verify())
):
    """
        Returns the results of the query
    """
    if isinstance(query, str): app_sql.run(query)
    else: app_sql.run_batch(query)
    return "success"

@app.post(
    "/rds/add",
    tags=["RDS"],
    summary="Adds one or multiple items to a given table",
)
async def rds_add(
    table: str = Body(..., embed=True, title="Name of the table"),
    item: Union[Dict, List[Dict]] = Body(..., embed=True, title="List of items to add"),
    current_user: User = Depends(app_jwt.verify())
):
    """
        Returns the results of the query
    """
    if isinstance(item, dict): app_sql.add(table, item)
    else: app_sql.add_batch(table, item)
    return "success"

# Tables routines

@app.get(
    "/rds/tables",
    tags=["RDS"],
    summary="Returns the list of tables",
)
async def rds_tables(
    current_user: User = Depends(app_jwt.verify())
):
    """
        Returns the schemas of all the available tables
    """
    return jsonable_encoder(app_sql.describe())

@app.post(
    "/rds/tables",
    tags=["RDS"],
    summary="Creates a new table",
)
async def rds_table_create(
    table: str = Body(..., embed=True, title="Name of the table"),
    schema: Dict = Body(..., embed=True, title="Schema of the table"),
    current_user: User = Depends(app_jwt.verify())
):
    """
        Returns the results of the query
    """
    app_sql.create_table(table, schema)
    return "success"

@app.delete(
    "/rds/tables",
    tags=["RDS"],
    summary="Deletes a table",
)
async def rds_table_delete(
    table: str = Body(..., embed=True, title="Name of the table"),
    current_user: User = Depends(app_jwt.verify())
):
    """
        Returns the results of the query
    """
    app_sql.delete_table(table)
    return "success"

# Handles the EFS warehouse
# @app.route('/warehouse', methods=['GET', 'DELETE'])
# @jwt_required()
# def warehouse():

#     def describe(path):

#         res, s_t = dict(), os.stat(path)
#         res['path'] = path
#         if S_ISDIR(s_t.st_mode):
#             res['type'] = 'directory'
#             res['items'] = {f : describe('/'.join([path, f])) for f in os.listdir(path)}
#         else:
#             res['type'] = 'file'
#         return res

#     if request.method == 'GET':
#         res = describe('./efs')
#     if request.method == 'DELETE':
#         for fle in os.listdir('./efs/warehouse'):
#             pth = '/'.join(['./efs/warehouse', fle])
#             if os.path.isdir(pth): shutil.rmtree(pth, ignore_errors=True)
#             else: os.remove(pth)
#         res = {'message': 'Action Completed'}
#     arg = {'status': 200, 'mimetype': 'application/json'}
#     return Response(json.dumps(res), **arg)

# Handles folders in the EFS warehouse
# @app.route('/warehouse/folder', methods=['POST', 'DELETE'])
# @jwt_required()
# def warehouse_folder():

#     cfg = request.get_json()
#     if request.method == 'POST':
#         os.makedirs(cfg.get('path'), exist_ok=True)
#         res = {'message': 'Action Completed'}
#     if request.method == 'DELETE':
#         shutil.rmtree(cfg.get('path'), ignore_errors=True)
#         res = {'message': 'Action Completed'}
#     arg = {'status': 200, 'mimetype': 'application/json'}
#     return Response(json.dumps(res), **arg)

# Route to create directory in EFS
# @app.route('/warehouse/file', methods=['POST', 'DELETE'])
# @jwt_required()
# def warehouse_file():

#     if request.method == 'POST':
#         cfg = request.args.get('path')
#         request.files.get('file').save(cfg)
#         res = {'message': 'Action Completed'}
#     if request.method == 'DELETE':
#         cfg = request.get_json()
#         os.remove(cfg.get('path'))
#         res = {'message': 'Action Completed'}
#     arg = {'status': 200, 'mimetype': 'application/json'}
#     return Response(json.dumps(res), **arg)
