class ResearchProviderError(Exception):
    """Base Exception for external research providers."""


class ResearchRateLimitError(ResearchProviderError):
    """Raised when a research provider rate-limits a request"""


class ResearchConnectionError(ResearchProviderError):
    """Raised when a research paper provider cannot be reached"""