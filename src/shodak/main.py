import logging

from shodak.config import settings
from shodak.logging_config import configure_logging

logger=logging.getLogger(__name__)

def  main()->None:
    configure_logging()

    logger.info(f"Starting {settings.app_name}")
    logger.info(f"Environment: {settings.environment}")


if __name__=="__main__":
    main()