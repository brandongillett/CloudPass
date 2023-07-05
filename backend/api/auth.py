from fastapi import Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from .config import SECRET_KEY,ALGORITHM,db
from .models import UserInDb,TokenData
from validate_email import validate_email

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def new_user(username: str, email: str, password: str):
    cursor = db.cursor()
    cursor.execute('SELECT * FROM Users WHERE username="{}"'.format(username))
    user=cursor.fetchone()
    cursor.execute('SELECT * FROM Users WHERE email="{}"'.format(email))
    em=cursor.fetchone()
    if not validate_email(email):
        cursor.close()
        return {"status":False,"message":"Invalid Email."}
    if len(password) < 8:
        cursor.close()
        return {"status":False,"message":"Password too short. (Min 8 characters)"}
    if len(username) > 30 or len(username) < 3:
        cursor.close()
        return {"status":False,"message":"Username too short. (Min 6 characters)"} if len(username) < 6 else {"status":False,"message":"Username too long. (Max 30 characters)"}
    if not user and not em:
        try:
            cursor = db.cursor()
            cursor.execute('INSERT INTO Users(username,email,disabled,password) VALUES(%s,%s,%s,%s)',(username,email,0,get_password_hash(password)))
            cursor.close()
            db.commit()
            return {"status":True,"message":f"{username} Created"}
        except:
            return {"status":False,"message":"An error has occured."}
    else:
        if user:
            cursor.close()
            return {"status":False,"message":"Username taken."}
        elif em:
            cursor.close()
            return {"status":False,"message":"Email taken."}

def get_user(username: str):
    cursor = db.cursor()
    cursor.execute('SELECT * FROM Users WHERE username="{}"'.format(username))
    user=cursor.fetchone()
    if user:
        user_data = {
            "id": user[0],
            "username": user[1],
            "email": user[2],
            "disabled": user[3],
            "password": user[4],
        }
        return UserInDb(**user_data)
    
def authenticate_user(username: str, password: str):
    user = get_user(username)
    if user and verify_password(password, user.password):
        return user
    return False

def create_access_token(data:dict, expires_delta: timedelta or None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credential_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                                         detail="Could not validate credentials", headers={"WWW-Authenticate":"Bearer"})
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credential_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credential_exception

    user = get_user(username=token_data.username)
    if user is None:
        raise credential_exception
    
    return user

async def get_current_active_user(current_user: UserInDb = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400,detail="Inactive user")
    return current_user