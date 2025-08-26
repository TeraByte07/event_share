from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    REFRESH_TOKEN_EXPIRE_MINUTES: int
    DATABASE_URL: str
    MEDIA_DIR: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()