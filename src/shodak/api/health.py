from shodak.config import settings


def get_provider_status()->list[dict[str,str|bool]]:
    return [
        {
            "provider":"groq",
            "configured":bool(settings.groq_api_key)
        },
        {
            "provider":"opneai",
            "configured":bool(settings.openai_api_key)
        }
    ]


def get_health_status()->str:
    providers=get_provider_status()
    if any(item["configured"] for item in providers):
        return "healthy"
    return "degraded"