from services.cities import Cities
from services.mysql import SqlHandler
from services.timestamp import Timestamps

sql_handler = SqlHandler()
city_manager = Cities(sql=sql_handler)
timestamps = Timestamps()
