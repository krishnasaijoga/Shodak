import logging
import time
from collections.abc import Iterator
from contextlib import contextmanager

logger=logging.getLogger("shodak")

@contextmanager
def log_operation(
    operation:str,
    **context:object
)->Iterator[None]:
    start=time.perf_counter()

    logger.info(
        "operation_started | operation=%s | context=%s",
        operation,
        context
    )

    try:
        yield
    except Exception:
        duration=time.perf_counter()-start

        logger.exception("operation_failed | operation=%s | duration=%.3f | context=%s",operation,duration,context)

        raise
    else:
        duration=time.perf_counter()-start

        logger.info(
            "operation_completed | operation=%s | duration=%.3f | context=%s",
            operation,
            duration,
            context
        )