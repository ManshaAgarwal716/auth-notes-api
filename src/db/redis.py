import redis.asyncio as redis
from src.config import set
EXPIRY_TIME=3600
token_blocklist=redis.StrictRedis(host=set.REDIS_HOST,port=set.REDIS_PORT,db=0)
async def add_token_to_blocklist(jti:str)-> None:
    await token_blocklist.set(
        name=jti,
        value="",
        ex=EXPIRY_TIME
    )
async def is_token_blocked(jti:str)->bool:
    result=await token_blocklist.get(jti)
    return result is not None