# Author:  Meryll Dindin
# Date:    November 04, 2020
# Project: CalAster

from src.utils import *

# Build webserver
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)

# Build helpers
app_sql = RDS()
app_efs = EFS()
app_s3b = S3B()
app_jwt = OAuth(oauth_scheme=OAuth2PasswordBearer(tokenUrl="/auth"))