from pydantic import BaseModel


class Settings(BaseModel):
    todoist_api_token: str | None = None
    openai_api_key: str | None = None
    openrouter_api_key: str | None = None
    
    model_provider: str = "openai"
    model_name: str = "gpt-4o-mini"
    
    whatsapp_session_path: str = "./auth"
    
    redis_url: str | None = None
    
    mock_todoist: bool = False


def load_settings() -> Settings:
    from os import getenv
    
    return Settings(
        todoist_api_token=getenv("TODOIST_API_TOKEN"),
        openai_api_key=getenv("OPENAI_API_KEY"),
        openrouter_api_key=getenv("OPENROUTER_API_KEY"),
        model_provider=getenv("MODEL_PROVIDER", "openai"),
        model_name=getenv("MODEL_NAME", "gpt-4o-mini"),
        whatsapp_session_path=getenv("WHATSAPP_SESSION_PATH", "./auth"),
        redis_url=getenv("REDIS_URL"),
        mock_todoist=getenv("MOCK_TODOIST", "false").lower() == "true",
    )


settings = load_settings()