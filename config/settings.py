from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int

settings = Settings(_env_file=".env")