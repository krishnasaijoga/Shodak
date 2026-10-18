from dataclasses import dataclass, field
from pathlib import Path

from shodak.config import settings


@dataclass
class StartupCheckResult:
    healthy:bool
    errors: list[str]=field(default_factory=list)
    warnings:list[str]=field(default_factory=list)


def validate_provider_configuration()->StartupCheckResult:
    errors:list=[]
    warnings:list[str]=[]

    groq_configured=bool(settings.groq_api_key)

    openai_configured=bool(settings.openai_api_key)

    if not groq_configured and not openai_configured:
        errors.append("No LLM provider API key is configured.")

    if settings.llm_provider=="groq" and not groq_configured:
        warnings.append("Primary provider 'groq' is not configured.")

    if settings.llm_provider=="openai" and not openai_configured:
        warnings.append("Primary provider 'openai' is not configured.")

    if settings.llm_fallback_provider=="groq" and not groq_configured:
        warnings.append("Fallback provider 'groq' is not configured.")

    if settings.llm_fallback_provider=="openai" and not openai_configured:
        warnings.append("Fallback provider 'openai' is not configured.")

    return StartupCheckResult(
        healthy=not errors,
        errors=errors,
        warnings=warnings
    )


def validate_filesystem_configuration()->StartupCheckResult:
    errors:list[str]=[]
    warnings:list[str]=[]

    if settings.run_history_enabled:
        path=Path(settings.run_history_path).expanduser()

        parent=path.parent

        try:
            parent.mkdir(parents=True,exist_ok=True)
        except OSError:
            errors.append("Run history directory cannot be created.")

    return StartupCheckResult(
        healthy=not errors,
        errors=errors,
        warnings=warnings
    )


def run_startup_checks()->StartupCheckResult:
    checks=[
        validate_provider_configuration(),
        validate_filesystem_configuration()
    ]

    errors:list[str]=[]
    warnings:list[str]=[]

    for check in checks:
        errors.extend(check.errors)
        warnings.extend(check.warnings)

    return StartupCheckResult(
        healthy= not errors,
        errors=errors,
        warnings=warnings
    )