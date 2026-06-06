from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.requests import Request
import time
import logging
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
logger=logging.getLogger("uvicorn.access")
logger.disabled=True
def register_middleware(app:FastAPI):
    @app.middleware("http")
    async def custom_logging(request:Request,call_next):
        start_time=time.time()
        response=await call_next(request)
        process_time=time.time()-start_time
        logger.info(f"Request: {request.method} {request.url} completed in {process_time:.2f} seconds")
        return response
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"]
    )
    app.add_middleware(
        TrustedHostMiddleware,  
        allowed_hosts=["*"]
    )