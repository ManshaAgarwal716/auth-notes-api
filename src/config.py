from pydantic_settings import BaseSettings,SettingsConfigDict
class Settings(BaseSettings):
    DATABASE_URL: str
    SYNC_DATABASE_URL:str
    JWT_SECRET:str
    JWT_ALGORITHM:str
    REDIS_HOST:str
    REDIS_PORT:int
    MAIL_USERNAME:str
    MAIL_PASSWORD:str
    MAIL_FROM:str
    MAIL_PORT:int
    MAIL_SERVER:str
    MAIL_STARTTLS:bool=True
    MAIL_SSL_TLS:bool=False
    USE_CREDENTIALS:bool=True
    VALIDATE_CERTS:bool=False
    model_config=SettingsConfigDict(env_file=".env",extra="ignore")
set=Settings()

