import os
from pathlib import Path

from dotenv import load_dotenv
from pydantic import BaseModel, Field, model_validator

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

    research_max_attempts:int=int(
        os.getenv(
            "RESEARCH_MAX_ATTEMPTS",
            "3"
        )
    )

    research_retry_inital_delay:float=float(
        os.getenv(
            "RESEARCH_RETRY_INITIAL_DELAY",
            "1.0"
        )
    )

    research_retry_backoff_multiplier:float=float(
        os.getenv(
            "RESEARCH_RETRY_BACKOFF_MULTIPLIER",
            "2.0"
        )
    )

    @model_validator(mode="after")
    def validate_settings(self):
        valid_providers={
            "groq",
            "openai"
        }

        if self.llm_provider not in valid_providers:
            raise ValueError(f"Unsupported LLM provider: {self.llm_provider}")

        if (self.llm_fallback_provider and self.llm_fallback_provider not in valid_providers):
            raise ValueError(f"Unsupported fallback LLM provider: {self.llm_fallback_provider}")

        if self.llm_max_attempts<1:
            raise ValueError("llm_max_attempts must be at least 1.")

        if self.llm_retry_initial_delay<0:
            raise ValueError("llm_retry_initial_delay cannot be neagtive.")

        if self.llm_retry_backoff_multiplier<1:
            raise ValueError("llm_retry_backoff_multiplier must be atleast 1.")

        if self.llm_max_concurrent_requests<1:
            raise ValueError("llm_max_concurrent_requests must be atleast 1.")

        if self.llm_min_request_interval_seconds<0:
            raise ValueError("llm_min_request_interval_seconds cannot be negative.")

        if self.research_cache_ttl_seconds<1:
            raise ValueError("research_cache_ttl_seconds must be atleast 1.")

        return self


settings=Settings()