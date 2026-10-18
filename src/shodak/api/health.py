from shodak.config import settings
from shodak.startup import run_startup_checks


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
    startup=run_startup_checks()
    status=("healthy" if startup.healthy else "degraded")
    providers=get_provider_status()
    if status=="healthy" and any(item["configured"] for item in providers):
        return "healthy"
    return "degraded"