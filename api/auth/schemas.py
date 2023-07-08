from pydantic import BaseModel, ConfigDict


class UserLogin(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    username: str
    email: str
    password: str

class User(UserLogin):
    id: int