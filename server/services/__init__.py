# Author:  Meryll Dindin
# Date:    November 04, 2020
# Project: CalAster

from services.cities import Cities
from services.database import SqlExecutor
from services.timestamp import Timestamps

sql_executor = SqlExecutor()
city_manager = Cities(sql=sql_executor)
timestamps = Timestamps()
