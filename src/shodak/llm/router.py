import logging

from pydantic import BaseModel

from shodak.config import settings
from shodak.llm.factory import get_llm_for_provider
from shodak.llm.rate_limit import get_provider_limiter
from shodak.llm.retry import run_with_retry
from shodak.usage import extract_token_usage, usage_tracker

logger=logging.getLogger("shodak.llm.router")


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
    if not llms:
        raise RuntimeError("No configured LLM providers are available.")
    return llms


def invoke_structured_with_fallback(
        schema:type[BaseModel],
        prompt:str
):
    last_error:Exception|None=None

    for provider,llm in get_llm_candidates():
        try:
            limiter=get_provider_limiter(
                            provider,
                            max_concurrent=settings.llm_max_concurrent_requests,
                            min_interval_seconds=settings.llm_min_request_interval_seconds
                        )
            structured_llm=llm.with_structured_output(schema)

            limiter=get_provider_limiter(provider,max_concurrent=settings.llm_max_concurrent_requests,min_interval_seconds=settings.llm_min_request_interval_seconds)

            def invoke_provider(limiter=limiter,structured_llm=structured_llm):
                with limiter.acquire():
                    return structured_llm.invoke(prompt)
            
            logger.info("llm_provider_attempt | provider=%s",provider)
            result=run_with_retry(
                operation=invoke_provider, 
                max_attempts=settings.llm_max_attempts,
                initial_delay=settings.llm_retry_initial_delay,
                backoff_multiplier=settings.llm_retry_backoff_multiplier,
                on_retry=lambda provider=provider: usage_tracker.record_retry(provider)
            )

            prompt_tokens,completion_tokens=extract_token_usage(result)

            usage_tracker.record_call(
                provider=provider,
                prompt_tokens=prompt_tokens,
                completion_tokens=completion_tokens
            )

            logger.info("llm_provider_success | provider=%s | prompt_tokens=%s | completion_tokens=%s",provider,prompt_tokens,completion_tokens)

            return result
        except Exception as exc: # noqa BLE001
            last_error=exc
            logger.warning("llm_provider_failed | provider=%s | error_type=%s", provider,type(exc).__name__)
    raise RuntimeError("All configured LLM providers failed.") from last_error