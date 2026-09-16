from pathlib import Path
import os

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


settings=Settings()