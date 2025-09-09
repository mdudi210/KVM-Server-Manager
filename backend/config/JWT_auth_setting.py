from fastapi_jwt_auth import AuthJWT
from pydantic import BaseModel
import os
from dotenv import load_dotenv

load_dotenv()

AUTHJWT_SECRET_KEY = os.getenv("AUTHJWT_SECRET_KEY")

class Settings(BaseModel):
    authjwt_secret_key: str = AUTHJWT_SECRET_KEY

settings = Settings()

@AuthJWT.load_config
def get_config():
    return settings