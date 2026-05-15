from passlib.context import CryptContext
pswd_context=CryptContext(schemes=["bcrypt"],deprecated="auto")
def generate_password_hash(password:str)->str:
    hash=pswd_context.hash(password)
    return hash
def verify_password(plain_password:str,hashed_password:str)->bool:
    return pswd_context.verify(plain_password,hashed_password)

