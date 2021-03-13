# Author:  Meryll Dindin
# Date:    November 04, 2020
# Project: CalAster

from src.imports import *

class User(BaseModel):

    id: str = Field(..., title="User ID")

class OAuth:

    def __init__(self, oauth_scheme=None):

        self.uid = os.getenv("JWT_USERNAME")
        self.pwd = os.getenv("JWT_PASSWORD")
        self.ot2 = oauth_scheme

    def authenticate(self, username: str, password: str):

        pwd = sha256(password.encode('utf-8')).hexdigest()
        if safe_str_cmp(username, self.uid) and safe_str_cmp(pwd, self.pwd):
            return User(**{'id': self.uid})
        return None

    def identity(self, packet: Dict):

        if safe_str_cmp(packet.get('identity'), self.uid):
            return User(**{'id': self.uid})
        return None

    def create_token(self, data: Dict):

        msg = deepcopy(data)
        dlt = timedelta(seconds=int(os.getenv("JWT_EXPIRATION_DELTA")))
        end = datetime.utcnow() + dlt
        msg.update({"exp": end})
        return jwt.encode(msg, os.getenv("JWT_SECRET_KEY"), algorithm="HS256")

    def verify(self):

        def verify_payload(token: str = Depends(self.ot2)):

            exception = HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )

            try:
                usr: User = self.identity(
                    jwt.decode(
                        token,
                        os.getenv("JWT_SECRET_KEY"),
                        algorithms=["HS256"]
                    )
                )
                if usr is None: raise exception
                return usr

            except Exception as e:
                raise exception
                return None

        return verify_payload
