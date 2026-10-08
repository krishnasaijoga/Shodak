
from pydantic import BaseModel

from shodak.config import settings
from shodak.llm.factory import get_llm_for_provider


def get_llm_candidates():
    providers=[settings.llm_provider]
    fallback=settings.llm_fallback_provider
    
    if fallback and fallback not in providers:
        providers.append(fallback)

    llms=[]
    for provider in providers:
        try:
            llm=get_llm_for_provider(provider)
            llms.append((provider,llm))
        except (ValueError,RuntimeError):
            continue
    if not llm:
        raise RuntimeError("No configured LLM providers are available.")
    return llm


def invoke_structured_with_fallback(
        schema:type[BaseModel],
        prompt:str
):
    last_error:Exception|None=None

    for _,llm in get_llm_candidates():
        try:
            structured_llm=llm.with_structured_output(schema)
            return structured_llm.invoke(prompt)
        except Exception as exc: # noqa BLE001
            last_error=exc
    raise RuntimeError("All configured LLM providers failed.") from last_error