from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/login")

_fake_users = {"admin": "admin"}
_fake_tokens = {"secrettoken": "admin"}

class User(BaseModel):
    username: str

def authenticate_user(username: str, password: str) -> str | None:
    if _fake_users.get(username) == password:
        return "secrettoken"
    return None

def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    username = _fake_tokens.get(token)
    if not username:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    return User(username=username)
