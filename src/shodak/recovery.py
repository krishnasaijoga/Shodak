import logging
from collections.abc import Callable

logger=logging.getLogger("shodak.recovery")


def run_optional[T](
        operation:Callable[[],T],
        *,
        operation_name:str,
        fallback:T
)->T:
    try:
        return operation()
    except Exception as exc: # noqa: BLE001
        logger.warning(
            "optional_operation_failed | operation=%s | error_style=%s",
            operation_name,
            type(exc).__name__
        )

    return fallback