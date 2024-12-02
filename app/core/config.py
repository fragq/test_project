from pydantic import BaseModel, PostgresDsn, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


class DatabaseSettings(BaseModel):
    HOST: str
    PORT: int
    USER: str
    PASS: str
    NAME: str
    DRIVER: str
    ECHO: bool = True
    ECHO_POOL: bool = False
    POOL_SIZE: int = 50
    MAX_OVERFLOW: int = 50
    NAMING_CONVENTION: dict[str, str] = {
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_N_name)s",
        "ck": "ck_%(table_name)s_`%(constraint_name)s`",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s",
    }

    @computed_field
    @property
    def SQLALCHEMY_DATABASE_URI(self) -> PostgresDsn:
        return f"{self.DRIVER}://{self.USER}:{self.PASS}@{self.HOST}:{self.PORT}/{self.NAME}"


class RunSettings(BaseModel):
    APP: str = "app.main:app"
    HOST: str = "127.0.0.1"
    PORT: int = 8000


class Settings(BaseSettings):

    model_config = SettingsConfigDict(
        env_file=(".env.example", ".env"),
        case_sensitive=False,
        env_nested_delimiter="__",
        env_ignore_empty=True,
    )

    db: DatabaseSettings
    run: RunSettings = RunSettings()


settings = Settings()
