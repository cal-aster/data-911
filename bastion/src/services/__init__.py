from fastapi.security import OAuth2PasswordBearer

from .auth import Authentication
from .rds import RdsHandler

authentication = Authentication(oauth_scheme=OAuth2PasswordBearer(tokenUrl="/oauth"))
rds_handler = RdsHandler()
