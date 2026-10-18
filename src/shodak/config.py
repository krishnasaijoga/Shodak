import os
from pathlib import Path

from dotenv import load_dotenv
from pydantic import BaseModel, Field

BASE_DIR=Path(__file__).resolve().parents[2]  # to get base directory of the project
ENV_FILE=BASE_DIR/".env"

load_dotenv(ENV_FILE)

class Settings(BaseModel):
    app_name:str="Shodak"
    
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

    llm_max_attempts:int=int(
        os.getenv(
            "LLM_MAX_ATTEMPTS",
            "3"
        )
    )

    llm_retry_initial_delay:float=float(
        os.getenv(
            "LLM_RETRY_INITIAL_DELAY",
            "0.5"
        )
    )

    llm_retry_backoff_multiplier:float=float(
        os.getenv(
            "LLM_RETRY_BACKOFF_MULTIPLIER",
            "2.0"
        )
    )

    cache_enabled:bool=(
        os.getenv(
            "CACHE_ENABLED",
            "true"
        ).lower()=="true"
    )

    research_cache_ttl_seconds:int=int(
        os.getenv(
            "RESEARCH_CACHE_TTL_SECONDS",
            "3600"
        )
    )

    llm_max_concurrent_requests:int=int(
        os.getenv(
            "LLM_MAX_CONCURRENT_REQUESTS",
            "3"
        )
    )

    llm_min_request_interval_seconds:float=float(
        os.getenv(
            "LLM_MIN_REQUEST_INTERVAL_SECONDS",
            "0.0"
        )
    )

    run_history_enabled:bool=(
        os.getenv("RUN_HISTORY_ENABLED","true").lower()=="true"
    )

    run_history_path:str=os.getenv(
        "RUN_HISTORY_PATH",
        "data/run_history.jsonl"
    )


settings=Settings()