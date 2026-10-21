import re
from pathlib import Path

MAX_TOPIC_LENGTH = 500
MAX_PROMPT_TEXT_LENGTH = 20_000

ALLOWED_OUTPUT_SUFFIXES = {".md", ".json"}

SECRET_PATTERNS = (
    re.compile(r"\bsk-[A-Za-z0-9_-]{10,}\b"),
    re.compile(r"\bgsk-[A-Za-z0-9_-]{10,}\b"),
)


def validate_topic(topic: str) -> str:
    cleaned = topic.strip()

    if not cleaned:
        raise ValueError("Topic cannot be empty.")

    if len(cleaned) > MAX_TOPIC_LENGTH:
        raise ValueError(f"Topic cannot exceed {MAX_TOPIC_LENGTH} characters.")

    return cleaned


def validate_text_length(
    value: str, *, field_name: str, max_length: int = MAX_PROMPT_TEXT_LENGTH
) -> str:
    if len(value) > max_length:
        raise ValueError(f"{field_name} cannot exceed {max_length} characters.")

    return value


def validate_output_path(output_path: str) -> Path:
    path = Path(output_path).expanduser()

    suffix = path.suffix.lower()

    if suffix not in ALLOWED_OUTPUT_SUFFIXES:
        raise ValueError("Output path must end in .md or .json")

    return path


def redact_secrets(value: str) -> str:
    redacted = value
    for pattern in SECRET_PATTERNS:
        redacted = pattern.sub("[REDACTED]", redacted)
    return redacted


def safe_error_message(exc: Exception) -> str:
    message = redact_secrets(str(exc))

    if len(message) > 500:
        message = message[:500] + "..."

    return message
