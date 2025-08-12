from fastapi_jwt_auth import AuthJWT
from pydantic import BaseModel

class Settings(BaseModel):
    authjwt_secret_key: str = "super-secret-key"  # Use a strong key in production

settings = Settings()

@AuthJWT.load_config
def get_config():
    return settings