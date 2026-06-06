from fastapi_mail import FastMail, MessageSchema, ConnectionConfig,MessageSchema, MessageType
from src.config import set
from pathlib import Path
BASE_dir=Path(__file__).resolve().parent
mail_config = ConnectionConfig(
    MAIL_USERNAME=set.MAIL_USERNAME,
    MAIL_PASSWORD=set.MAIL_PASSWORD,
    MAIL_FROM=set.MAIL_FROM,
    MAIL_PORT=set.MAIL_PORT,
    MAIL_SERVER=set.MAIL_SERVER,
    MAIL_STARTTLS=set.MAIL_STARTTLS,
    MAIL_SSL_TLS=set.MAIL_SSL_TLS,
    USE_CREDENTIALS=set.USE_CREDENTIALS,
    VALIDATE_CERTS=set.VALIDATE_CERTS,
    TEMPLATE_FOLDER=BASE_dir / "templates"
)
mail=FastMail(
    config=mail_config
)
def create_message(recipients:list,subject:str,body:str)->MessageSchema:
    message=MessageSchema(
        subject=subject,
        recipients=recipients,
        subtype=MessageType.html,
        body=body
    )
    return message