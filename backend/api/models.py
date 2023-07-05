from pydantic import BaseModel

class Token(BaseModel):
    status: str
    access_token: str
    token_type: str
    fernet_key: str

class TokenData(BaseModel):
    username: str or None = None

class NewUser(BaseModel):
    username: str
    email: str
    password: str

class User(BaseModel):
    id: int
    username: str
    email: str or None = None
    disabled: bool or None = None

class UserInDb(User):
    password: str