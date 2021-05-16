from pydantic import BaseModel, Field


class UserModel(BaseModel):

    id: str = Field(..., title="User ID")


class LoginPayload(BaseModel):

    username: str = Field(..., title="User's username")
    password: str = Field(..., title="User's password")
