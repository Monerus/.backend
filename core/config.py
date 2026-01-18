from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path
import psycopg2
BASE_DIR = Path(__file__).resolve().parent.parent

class Settings(BaseSettings):
    
    
    #JWT
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    REFRESH_TOKEN_EXPIRE_DAYS: int = 30
    PRIVATE_KEY_PATH: Path = BASE_DIR / "certs" / "private_key.pem"
    PUBLIC_KEY_PATH: Path = BASE_DIR / "certs" / "public_key.pem"
    JWT_ALGORITHM: str
    
    #POSTGRES
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    DB_ECHO: bool = False
    POSTGRES_CONNECT: str
    
    #REDIS
    # REDIS_HOST: str
    # REDIS_PORT: int
    # REDIS_PASSWORD: str
    # REDIS_DB: int
       
    @property
    def db_url(self) -> str:
        return (
            f"postgresql+asyncpg://"
            f"{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.POSTGRES_CONNECT}/{self.POSTGRES_DB}"
        )
        # return  (
        #     f"postgresql+asyncpg://db_q6ew_user:lmXIW3j8eJlAiFHa2IY1HnsG1cAFBdg1@dpg-d56s6ure5dus73cvlemg-a.oregon-postgres.render.com/db_q6ew"
        #     )
        
    model_config = SettingsConfigDict(env_file=".env", extra='ignore', env_file_encoding='utf-8')

settings = Settings()