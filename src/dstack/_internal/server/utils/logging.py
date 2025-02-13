import asyncio
import logging
import os
import sys

from dstack._internal.server import settings


class AsyncioCancelledErrorFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        if record.exc_info is None:
            return True
        if isinstance(record.exc_info[1], asyncio.CancelledError):
            return False
        return True


def configure_logging():
    root_logger = logging.getLogger(None)
    handler = logging.StreamHandler(stream=sys.stdout)
    handler.addFilter(AsyncioCancelledErrorFilter())
    formatter = logging.Formatter(
        fmt="%(levelname)s %(asctime)s.%(msecs)03d %(name)s %(message)s",
        datefmt="%Y-%m-%dT%H:%M:%S",
    )
    handler.setFormatter(formatter)
    root_logger.addHandler(handler)
    root_logger.setLevel(settings.ROOT_LOG_LEVEL)
    dstack_logger = logging.getLogger("dstack")
    dstack_logger.setLevel(settings.LOG_LEVEL)
