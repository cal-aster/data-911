# Author:  Meryll Dindin
# Date:    November 04, 2020
# Project: CalAster

from services.cities import Cities
from services.database import SqlHandler
from services.timestamp import Timestamps

sql_handler = SqlHandler()
city_manager = Cities(sql=sql_handler)
timestamps = Timestamps()
