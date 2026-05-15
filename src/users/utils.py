from passlib.context import CryptContext
from datetime import timedelta,datetime
import uuid
from jose import jwt, JWTError
import logging
from src.config import set
pswd_context=CryptContext(schemes=["bcrypt"],deprecated="auto")
ACCESS_TOKEN_EXPIRY=3600
def generate_password_hash(password:str)->str:
    hash=pswd_context.hash(password)
    return hash
def verify_password(plain_password:str,hashed_password:str)->bool:
    return pswd_context.verify(plain_password,hashed_password)
def create_access_token(user_data:dict,expiry:timedelta=None,refresh:bool=False)->str:
    payload={}
    payload["user"]=user_data
    payload["exp"]=datetime.now()+expiry if expiry else datetime.now()+timedelta(seconds=ACCESS_TOKEN_EXPIRY)
    payload["refresh"]=refresh
    payload['jti']=str(uuid.uuid4())
    token=jwt.encode(payload,set.JWT_SECRET,algorithm=set.JWT_ALGORITHM)
    return token
def decode_access_token(token:str)->dict:
    try:
        token_data=jwt.decode(token,set.JWT_SECRET,algorithms=[set.JWT_ALGORITHM])  
        return token_data
    except JWTError as e:
        logging.error(f"Token decoding error: {e}")
        return None
    






