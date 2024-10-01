from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    postgres_db: str
    postgres_user: str
    postgres_password: str
    postgres_host: str
    postgres_port: str

    model_config = SettingsConfigDict(env_file=".env", extra="allow")

    @property
    def database_url(self):
        return f"postgresql+asyncpg://{self.postgres_user}:{self.postgres_password}@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"


settings = Config()
