from pydantic import Field
from pydantic_settings import BaseSettings
from sqlalchemy.engine import URL
from functools import lru_cache


class Settings(BaseSettings):

    APP_NAME: str = "Auth Service"
    APP_PORT: int = Field(default=8000)

    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_PORT: str
    POSTGRES_DB: str  

    @property
    def SQLALCHEMY_DATABASE_URI(self) -> str:
        return URL.create(
            drivername="postgresql+psycopg2",
            username=self.POSTGRES_USER,
            password=self.POSTGRES_PASSWORD,
            host=self.POSTGRES_HOST,
            port=self.POSTGRES_PORT,
            database=self.POSTGRES_DB,
        ).render_as_string(hide_password=False)

    JWT_SECRET: str
    JWT_ALGORITHM: str = Field(default="HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(default=60)
    PASSWORD_HASH_ALGORITHM: str = Field(default="bcrypt")
    # REDIS_HOST: str = Field(default="localhost")
    # REDIS_PORT: int = Field(default=6379)

    class Config:
        env_file = ".env"
        case_sensitive = True
        extra = "ignore"


# Singleton settings instance
@lru_cache()
def get_settings() -> Settings:
    return Settings()