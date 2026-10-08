import os
from pathlib import Path

from dotenv import load_dotenv
from pydantic import BaseModel, Field

BASE_DIR=Path(__file__).resolve().parents[2]  # to get base directory of the project
ENV_FILE=BASE_DIR/".env"

load_dotenv(ENV_FILE)

class Settings(BaseModel):
    app_name:str="shodak"
    environment:str=Field(
        default_factory= lambda: os.getenv("APP_ENV","development")
    )
    log_level:str=Field(
        default_factory=lambda:os.getenv("LOG_LEVEL","INFO")
    )
    openai_api_key:str|None=Field(default_factory=lambda:os.getenv("OPENAI_API_KEY"))
    openai_model:str=Field(
            default_factory=lambda: os.getenv(
            "OPENAI_MODEL",
            "gpt-5-mini"
        )
    )
    llm_provider:str=Field(
        default_factory=lambda:os.getenv(
            "LLM_PROVIDER",
            "groq"
        )
    )
    groq_api_key:str|None=Field(
        default_factory=lambda: os.getenv(
            "GROQ_API_KEY"
        )
    )
    groq_model:str=Field(
        default_factory=lambda:os.getenv(
            "GROQ_MODEL",
            "openai/gpt-oss-120b"
        )
    )
    llm_fallback_provider:str|None=os.getenv(
        "LLM_FALLBACK_PROVIDER",
        "openai"
    )


settings=Settings()