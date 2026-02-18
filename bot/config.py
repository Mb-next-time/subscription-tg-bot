from pydantic_settings import BaseSettings, SettingsConfigDict

class CommonSettings(BaseSettings):
    BOT_TOKEN: str

    model_config = SettingsConfigDict(env_file=".env")