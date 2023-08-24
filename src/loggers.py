"""
Basic logging
"""
import logging
import re
import sys
from pathlib import Path

from src import ROOT_DIR


# https://docs.python.org/3/library/logging.html#:~:text=available%20to%20you.-,Attribute%20name,-Format
_common_format = "%(asctime)s %(levelname)s %(name)s:%(lineno)d - %(message)s"


def _clip_module(module: str) -> str:
    """Convert the input module to a relative path from the repo root"""
    try:
        return str(Path(module).relative_to(ROOT_DIR))
    except ValueError:
        # the module is being used as a name, like hopefully only use of logging in Jupyter Notebooks causes
        return module


def stream_logger(module: str, stream=sys.stdout) -> logging.Logger:
    logger = logging.getLogger(_clip_module(module))

    # getLogger returns the same logger object as determined by name
    if logger.hasHandlers():
        return logger

    formatter = logging.Formatter(fmt=_common_format)
    handler = logging.StreamHandler(stream=stream)
    handler.setFormatter(fmt=formatter)

    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)

    return logger


if __name__ == "__main__":
    logger = stream_logger(__file__)
    logger.info("Testing testing!")
