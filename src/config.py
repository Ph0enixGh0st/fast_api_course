from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DB_NAME: str
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASSWORD: str

    @property
    def DATABASE_URL(self):
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"


    model_config = SettingsConfigDict(env_file=".env")  #, extra="ignore"



settings = Settings()