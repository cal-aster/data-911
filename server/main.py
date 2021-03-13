# Author:  Meryll Dindin
# Date:    November 04, 2020
# Project: CalAster

from routers import cities, general, spatial, temporal
from src.helpers import *

### Routes

app.include_router(cities.router, prefix="/city", tags=["city"])

app.include_router(general.router, tags=["base"])

app.include_router(spatial.router, prefix="/spatial", tags=["spatial"])

app.include_router(temporal.router, prefix="/temporal", tags=["temporal"])
