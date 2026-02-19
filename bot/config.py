from pydantic_settings import BaseSettings, SettingsConfigDict

class BotSettings(BaseSettings):
    TOKEN: str

    model_config = SettingsConfigDict(env_file=".env.bot", env_prefix="BOT_")