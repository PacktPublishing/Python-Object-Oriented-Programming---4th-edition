"""
Python 3 Object-Oriented Programming

Chapter 10. The iterator pattern
"""
from __future__ import annotations
import argparse
import logging
import sys
from textwrap import dedent
import time

def make_log_messages(base_delay: float = 6, multiline: bool = True) -> None:
    logger = logging.getLogger("sample")
    logger.debug("This is a debugging message.")
    time.sleep(base_delay*2)
    logger.info("This is an information method.")
    time.sleep(base_delay*2)
    logger.warning("This is a warning. It could be serious.")
    time.sleep(base_delay)
    logger.warning("Another warning sent.")
    time.sleep(base_delay)
    logger.info("Here's some information.")

    if multiline:
        time.sleep(base_delay/2)
        logger.info(
            dedent("""
                This is a multi-line information
                message, with misleading content including WARNING
                and it spans lines of the log file WARNING used in a confusing way
            """
            ).strip()
        )

    time.sleep(base_delay*2)
    logger.debug("Debug messages are only useful if you want to figure something out.")
    time.sleep(base_delay*2)
    logger.info("Information is usually harmless, but helpful.")
    time.sleep(base_delay)
    logger.warning("Warnings should be heeded.")
    time.sleep(base_delay)
    logger.warning("Watch for warnings.")


def get_options(argv: list[str] = sys.argv[1:]) -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("-m", "--multiline", action="store_const", const=True, default=False)
    parser.add_argument("-d", "--delay", action="store", type=float, default=6)
    return parser.parse_args(argv)


if __name__ == "__main__":
    datefmt = "%b %d, %Y %X"
    format = "%(asctime)s %(levelname)s %(message)s"
    logging.basicConfig(level=logging.DEBUG, format=format, datefmt=datefmt)
    options = get_options()
    make_log_messages(base_delay=options.delay, multiline=options.multiline)
