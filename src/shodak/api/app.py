from fastapi import FastAPI

from shodak.config import settings

app=FastAPI(
    title="Shodak API",
    description="Research and Writing API powered by Shodak's multi-agent workflow.",
    version="0.1.0"
)


@app.get("/")
def root()->dict[str,str]:
    return {
        "name":settings.app_name,
        "status":"running"
    }


@app.get("/health")
def health()->dict[str,str]:
    return {
        "status":"healthy",
        "environment":settings.environment
    }