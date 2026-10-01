from langchain_core.language_models.chat_models import BaseChatModel
from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI

from shodak.config import settings


def _get_groq_llm()->BaseChatModel:
    if not settings.groq_api_key:
        raise ValueError(
            "GROQ_API_KEY is not configured"
        )
    return ChatGroq(
        model=settings.groq_model,
        api_key=settings.groq_api_key,
        temperature=0
    )


def _get_openai_llm()->BaseChatModel:
    if not settings.openai_api_key:
        raise ValueError("OPENAI_API_KEY is not configured")
    return ChatOpenAI(
        model=settings.openai_model,
        api_key=settings.openai_api_key,
        temperature=0
    )


def get_llm()->BaseChatModel:
    provider=settings.llm_provider.lower().strip()

    if provider=="groq":
        return _get_groq_llm()
    if provider=="openai":
        return _get_openai_llm()
    raise ValueError(
        f"Unsupported LLM provider: {settings.llm_provider}"
    )